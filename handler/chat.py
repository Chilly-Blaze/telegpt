from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from util import CHAT


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message is not None
    reply = ''.join(context.bot_data['chat'].ask_stream(update.message.text))
    await update.message.reply_text(reply)
    return CHAT


chat_handler = MessageHandler(filters.TEXT & ~(filters.COMMAND), chat)
