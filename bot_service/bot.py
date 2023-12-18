from os import getenv
import logging

import bot_service.handlers as hdl

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

def create_bot_app():
    telegram_token = getenv("TELEGRAM_TOKEN")
    if not telegram_token:
        logging.error("Cannot start bot without TELEGRAM_TOKEN env variable defined.")
        raise ValueError("Cannot start bot without TELEGRAM_TOKEN env variable defined.")
    app = Application.builder().token(telegram_token).build()
    app.add_handler(CommandHandler("start", hdl.show_intro))
    # TODO: add error handler with fallback to the team chat
    return app

if __name__ == "__main__":
    bot = create_bot_app()
    bot.run_polling()
