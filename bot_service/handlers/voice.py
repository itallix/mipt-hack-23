import logging
import tempfile
from os import getenv

from google.api_core.client_options import ClientOptions
from google.cloud import firestore, texttospeech
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from langdetect import detect
from telegram import Update
from telegram.ext import ContextTypes
from vertexai.preview.generative_models import GenerationConfig, GenerativeModel

from bot_service.utils.actions import send_upload_voice_action
from bot_service.utils.chat_history import from_json, to_json
from bot_service.utils.markdown import markdown_to_text

CHATS = "Chats"
TEXTTOSPEECH_PARAMS = {
    "ru": {
        "language_code": "ru-RU",
        "name": "ru-RU-Wavenet-D",
        "ssml_gender": texttospeech.SsmlVoiceGender.MALE,
    },
    "en": {
        "language_code": "en-US",
        "name": "en-US-Wavenet-J",
        "ssml_gender": texttospeech.SsmlVoiceGender.MALE,
    },
}


def _transcribe_audio(content: bytes) -> str:
    """Transcribes audio to text using Google's speech API.

    Args:
        content: Binary audio content that needs to be transcribed.

    Returns:
        A text that represents the audio.
    """
    logging.info("Transcribing audio...")
    client = SpeechClient(
        client_options=ClientOptions(
            api_endpoint="us-central1-speech.googleapis.com",
        )
    )

    # TODO: move to GCS (currently limited with 60sec)
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["auto"],
        model="chirp",
    )
    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{getenv('PROJECT_ID')}/locations/us-central1/recognizers/_",
        config=config,
        content=content,
    )
    response = client.recognize(request)
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript
        logging.debug(f"Transcript: {result.alternatives[0].transcript}")
        logging.debug(f"Confidence: {result.alternatives[0].confidence}")

    logging.info(f"Transcription finished: {transcript}")
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
    logging.info("Generating audio...")
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    lang_code = detect(text)
    voice = texttospeech.VoiceSelectionParams(**TEXTTOSPEECH_PARAMS.get(lang_code))
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.OGG_OPUS
    )
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    filename = f"{tmp_dir}/{update_id}.ogg"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
    logging.info(f"Audio generated: {filename}")
    return filename


@send_upload_voice_action
async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for voice messages that combines all APIs together."""
    msg = update.effective_message
    with tempfile.TemporaryDirectory(prefix="/tmp/") as tmp_dir:
        audio_file = await msg.voice.get_file()
        ogg_filename = f"{tmp_dir}/{audio_file.file_id}.ogg"
        await audio_file.download_to_drive(ogg_filename)
        with open(ogg_filename, "rb") as audio_file:
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
            await msg.reply_voice(audio_file_path, write_timeout=40)
            if doc.exists:
                doc_ref.update(
                    {"history": firestore.ArrayUnion(to_json(chat.history[-2:]))}
                )
            else:
                doc_ref.set({"history": to_json(chat.history)})
