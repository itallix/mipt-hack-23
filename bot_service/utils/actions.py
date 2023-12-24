from functools import wraps

from telegram import Update
from telegram.constants import ChatAction


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update: Update, *args, **kwargs):
            bot = update.get_bot()
            chat_id = update.effective_message.chat_id
            await bot.send_chat_action(chat_id=chat_id, action=action)
            return await func(update, *args, **kwargs)

        return command_func

    return decorator


send_typing_action = send_action(ChatAction.TYPING)
send_upload_voice_action = send_action(ChatAction.UPLOAD_VOICE)
