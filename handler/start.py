from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from chatapi import ChatManager
from log import INFO, log, statics
from util import CHAT


# /start [key]
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message
    user = update.message.from_user
    if context.args and context.args[0] == context.bot_data['token']:
        manager: ChatManager = context.bot_data['manager']
        manager.new(user)
        await update.message.reply_text(context.bot_data['hint']['start'])
        log(user, statics.access.format(len(manager.list_())))
        return CHAT
    log(user, statics.start, INFO)
    await update.message.reply_text(context.bot_data['hint']['welcome'])
    return


start_handler = CommandHandler('start', start)
