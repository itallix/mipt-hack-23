from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes
from vertexai.preview.generative_models import GenerationConfig, GenerativeModel

DEFAULT_PROMPT = {
    "ru": "Расскажи мне забавный факт о случайном городе",
    "en": "Tell me a fun fact about some random city",
}


async def handle_random_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /story command that asks Gemini Pro to generate a random story
    
    A prompt will be used based on the user's profile language code.
    """    
    msg = update.message
    await context.bot.send_chat_action(chat_id=msg.chat_id, action=ChatAction.TYPING)
    model = GenerativeModel('gemini-pro')
    prompt = DEFAULT_PROMPT.get(msg.from_user.language_code, "en")
    response = model.generate_content(
                prompt,
                generation_config=GenerationConfig(
                    temperature=0.9, top_k=40, top_p=0.5
                ),
            )
    await msg.reply_html(f"{response.text}")
    
    