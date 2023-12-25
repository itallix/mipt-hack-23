from flask import Flask, request
from telegram import Update
from telegram.ext import Application

from bot_service.bot import create_bot_app

app = Flask(__name__)
bot_app: Application = create_bot_app()


@app.post("/")
async def index() -> str:
    async with bot_app:
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        await bot_app.process_update(update)

    return "ok"
