import logging
from os import getenv

from telegram.ext import Application, CommandHandler, MessageHandler, filters

import bot_service.handlers as hdl


def create_bot_app():
    telegram_token = getenv("TELEGRAM_TOKEN")
    if not telegram_token:
        logging.error("Cannot start bot without TELEGRAM_TOKEN env variable defined.")
        raise ValueError(
            "Cannot start bot without TELEGRAM_TOKEN env variable defined."
        )
    app = Application.builder().token(telegram_token).build()
    app.add_handler(CommandHandler("start", hdl.show_intro))
    app.add_handler(MessageHandler(filters.VOICE, hdl.handle_voice_message))
    app.add_handler(MessageHandler(filters.PHOTO, hdl.handle_photo_message))
    # TODO: add error handler with fallback to the team chat
    return app


if __name__ == "__main__":
    bot = create_bot_app()
    bot.run_polling()
