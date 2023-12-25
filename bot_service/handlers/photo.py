import tempfile

from telegram import Update
from telegram.ext import ContextTypes
from vertexai.preview.generative_models import GenerationConfig, GenerativeModel, Image

from bot_service.utils.actions import send_typing_action

DEFAULT_PROMPT = {
    "ru": "Расскажи мне историю о том, что здесь изображено",
    "en": "Tell me the story about what is depicted here",
}


@send_typing_action
async def handle_photo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for photo messages that asks Gemini Pro Vision to generate a story about the photo.

    If the user doesn't provide a caption, a default prompt based on the user's profile language
    code will be used.
    """
    msg = update.effective_message
    prompt = msg.caption or DEFAULT_PROMPT[msg.from_user.language_code]
    with tempfile.TemporaryDirectory(prefix="/tmp/") as tmp_dir:
        file_path = f"{tmp_dir}/{msg.id}.jpg"
        file_id = msg.photo[-1].file_id
        file = await context.bot.get_file(file_id)
        await file.download_to_drive(file_path)
        with open(file_path, "rb") as f:
            img = Image.from_bytes(f.read())
            model = GenerativeModel("gemini-pro-vision")
            response = model.generate_content(
                [img, prompt],
                generation_config=GenerationConfig(
                    temperature=0.9, top_k=40, top_p=0.5
                ),
            )
            await msg.reply_markdown(response.text)
