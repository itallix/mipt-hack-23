import tempfile

from google.cloud import firestore, speech, texttospeech
from pydub import AudioSegment
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes
from vertexai.preview.generative_models import GenerationConfig, GenerativeModel

from bot_service.utils.chat_history import from_json, to_json
from bot_service.utils.markdown import markdown_to_text

CHATS = "Chats"


def _transcribe_audio(content: bytes) -> str:
    """Transcribes audio to text using Google's speech API.

    Args:
        content: Binary audio content that needs to be transcribed.

    Returns:
        A text that represents an audio.
    """
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=content)

    # TODO: move to GCS (currently limited with 60sec)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code="ru-RU",
    )
    response = client.recognize(config=config, audio=audio)
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript
        print(f"Transcript: {result.alternatives[0].transcript}")
        print(f"Confidence: {result.alternatives[0].confidence}")

    return transcript


def _get_audio_from_text(tmp_dir: str, update_id: int, text: str) -> str:
    """Generates audio based on text using Google's texttospeech API.

    Args:
        tmp_dir: Temp directory served as cache for generated audio files.
        update_id: Unique ID of the current update that used to construct filename.
        text: Text that needs to be synthesized as audio.

    Returns:
        A path to the generated audio file
    """
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ru-RU",
        name="ru-RU-Wavenet-D",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    filename = f"{tmp_dir}/{update_id}.mp3"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
    return filename


async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for voice messages that combines all pieces together."""
    msg = update.effective_message
    await context.bot.send_chat_action(
        chat_id=msg.chat_id, action=ChatAction.UPLOAD_VOICE
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        audio_file = await msg.voice.get_file()
        ogg_filename = f"{tmp_dir}/{audio_file.file_id}.ogg"
        ogg_audio = await audio_file.download_to_drive(ogg_filename)
        voice = AudioSegment.from_ogg(ogg_audio)
        mp3_filename = f"{tmp_dir}/{audio_file.file_id}.mp3"
        voice.export(mp3_filename, format="mp3")
        with open(mp3_filename, "rb") as audio_file:
            transcript = _transcribe_audio(audio_file.read())
            client = firestore.Client()
            doc_ref = client.collection(CHATS).document(str(msg.chat_id))
            doc = doc_ref.get()
            model = GenerativeModel("gemini-pro")
            chat = model.start_chat(history=from_json(doc.get("history")))
            response = chat.send_message(
                transcript,
                generation_config=GenerationConfig(
                    temperature=0.9, top_k=40, top_p=0.5
                ),
            )
            audio_file_path = _get_audio_from_text(
                tmp_dir, update.update_id, markdown_to_text(response.text)
            )
            await msg.reply_voice(audio_file_path)
            if doc.exists:
                doc_ref.update(
                    {"history": firestore.ArrayUnion(to_json(chat.history[-2:]))}
                )
            else:
                doc_ref.set({"history": to_json(chat.history)})
