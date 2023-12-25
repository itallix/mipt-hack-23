from telegram import Update
from telegram.ext import ContextTypes


async def show_intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    name = msg.chat.first_name or msg.chat.title
    await msg.reply_html(f"Welcome {name}!")
