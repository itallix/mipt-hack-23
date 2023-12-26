from random import choice

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes
from vertexai.preview.generative_models import GenerationConfig, GenerativeModel

CITIES = {
    "ru": [
        "Нью-Йорк",
        "Лондон",
        "Париж",
        "Токио",
        "Сингапур",
        "Гонконг",
        "Сеул",
        "Шанхай",
        "Дубай",
        "Мельбурн",
        "Цюрих",
        "Копенгаген",
        "Вена",
        "Мюнхен",
        "Бангкок",
        "Торонто",
        "Окленд",
        "Франкфурт",
        "Женева",
        "Амстердам",
        "Брюссель",
        "Дублин",
        "Осака",
        "Москва",
        "Санкт-Петербург",
        "Прага",
        "Хельсинки",
        "Лиссабон",
        "Будапешт",
        "Варшава",
        "Рейкьявик",
    ],
    "en": [
        "New York",
        "London",
        "Paris",
        "Tokyo",
        "Singapore",
        "Hong Kong",
        "Seoul",
        "Shanghai",
        "Dubai",
        "Melbourne",
        "Zurich",
        "Copenhagen",
        "Vienna",
        "Munich",
        "Bangkok",
        "Toronto",
        "Auckland",
        "Frankfurt",
        "Geneva",
        "Amsterdam",
        "Brussels",
        "Dublin",
        "Osaka",
        "Moscow",
        "Saint Petersburg",
        "Prague",
        "Helsinki",
        "Lisbon",
        "Budapest",
        "Warsaw",
        "Reykjavík",
    ],
}


async def handle_random_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /story command that asks Gemini Pro to generate a random story

    A prompt will be used based on the user's profile language code.
    """
    DEFAULT_PROMPT = {
        "ru": f"Расскажи мне забавный факт о городе {choice(CITIES['ru'])}",
        "en": f"Tell me a fun fact about {choice(CITIES['en'])}",
    }

    msg = update.message
    await context.bot.send_chat_action(chat_id=msg.chat_id, action=ChatAction.TYPING)
    model = GenerativeModel("gemini-pro")
    prompt = DEFAULT_PROMPT.get(msg.from_user.language_code, "en")
    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(temperature=0.9, top_k=40, top_p=0.5),
    )
    await msg.reply_html(f"{response.text}")
