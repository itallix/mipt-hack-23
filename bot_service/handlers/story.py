from random import choice

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes
from vertexai.preview.generative_models import GenerationConfig, GenerativeModel

cities_ru = [
    "Токио",
    "Чунцин",
    "Дели",
    "Шанхай",
    "Дакка",
    "Сан-Паулу",
    "Мехико",
    "Нью-Йорк",
    "Мумбаи",
    "Манила",
    "Сеул",
    "Пекин",
    "Брисбен",
    "Чэнду",
    "Сидней",
    "Тяньцзинь",
    "Мельбурн",
    "Киншаса",
    "Ухань",
    "Стамбул",
    "Далоа",
    "Анкоридж",
    "Дубай",
    "Москва",
    "Аделаида",
    "Бамако",
    "Александрия",
    "Баку",
    "Габу",
    "Давао",
]

cities_en = [
    "Tokyo",
    "Chongqing",
    "Delhi",
    "Shanghai",
    "Dhaka",
    "Sao Paulo",
    "Mexico City",
    "New York",
    "Mumbai",
    "Manila",
    "Seoul",
    "Beijing",
    "Brisbane",
    "Chengdu",
    "Sydney",
    "Tianjin",
    "Melbourne",
    "Kinshasa",
    "Wuhan",
    "Istanbul",
    "Daloa",
    "Anchorage",
    "Dubai",
    "Moscow",
    "Adelaide",
    "Bamako",
    "Alexandria",
    "Baku",
    "Gabu",
    "Davao",
]

DEFAULT_PROMPT = {
    "ru": f"Расскажи мне забавный факт о городе {choice(cities_ru)}",
    "en": f"Tell me a fun fact about {choice(cities_en)}",
}


async def handle_random_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /story command that asks Gemini Pro to generate a random story

    A prompt will be used based on the user's profile language code.
    """
    msg = update.message
    await context.bot.send_chat_action(chat_id=msg.chat_id, action=ChatAction.TYPING)
    model = GenerativeModel("gemini-pro")
    prompt = DEFAULT_PROMPT.get(msg.from_user.language_code, "en")
    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(temperature=0.9, top_k=40, top_p=0.5),
    )
    await msg.reply_html(f"{response.text}")
