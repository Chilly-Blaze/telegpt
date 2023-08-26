from telegram import Message, Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters
from chatapi import ChatManager
from log import WARN, log, statics
from util import CHAT


# TEXT resp
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message and context.chat_data is not None
    send = update.message.text
    user = update.message.from_user
    msg = await update.message.reply_text(context.bot_data['hint']['chat'])
    log(user, statics.chat_s.format(send))
    manager: ChatManager = context.bot_data['manager']
    reply = manager.get(user).talk(send)
    context.chat_data['last'] = await msg.edit_text(reply)
    log(user, statics.chat_r.format(reply))
    return CHAT


# /regenerate
async def regenerate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert context.chat_data is not None
    msg: Message | None = context.chat_data.get('last')
    assert update.message
    user = update.message.from_user
    if msg is None:
        await update.message.reply_text(context.bot_data['hint']['regenerate_fail'])
        log(user, statics.regenerate_f, WARN)
    else:
        await update.message.delete()
        await msg.edit_text(context.bot_data['hint']['regenerate'])
        manager: ChatManager = context.bot_data['manager']
        reply = manager.get(user).regenerate()
        await msg.edit_text(reply)
        log(user, statics.regenerate_s.format(msg.text))
    return CHAT


chat_handler = MessageHandler(filters.TEXT & ~(filters.COMMAND), chat)
regenerate_handler = CommandHandler('regenerate', regenerate)
