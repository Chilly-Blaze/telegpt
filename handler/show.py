from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler
from util import CHAT, choose_template, SHOW, match


async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = context.bot_data['hint']['show_choose']
    await choose_template(update, context, text)
    return SHOW


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    assert query is not None
    text = context.bot_data['prompt'][query.data]
    await query.answer()
    await query.edit_message_text(text=text)
    return CHAT


async def show_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.bot_data['mode']
    if mode != 'none':
        text = ''
    else:
        text = context.bot_data['prompt'][mode]
    assert update.message is not None
    await update.message.reply_text(text=text)
    return CHAT


show_handler = CommandHandler('show', show)
now_handler = CommandHandler('now', show_me)
show_callback = CallbackQueryHandler(callback, match)
