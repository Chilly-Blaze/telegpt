from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from util import CHAT


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.effective_chat is not None
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=context.bot_data['hint']['start'])
    return CHAT


start_handler = CommandHandler('start', start)
