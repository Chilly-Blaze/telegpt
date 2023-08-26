from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler
from chatapi import ChatManager
from log import log, statics
from util import CHAT, get_prompt, plain_text, prompt_buttons, SHOW


# /show
async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message is not None
    text = context.bot_data['hint']['show_choose']
    await update.message.reply_text(text, reply_markup=prompt_buttons())
    return SHOW


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    assert query is not None
    user = query.from_user
    mode = query.data
    text = plain_text(get_prompt(mode))
    await query.answer()
    await query.edit_message_text(
        context.bot_data['hint']['show'].format(mode, text), ParseMode.HTML
    )
    log(user, statics.show.format(query.data))
    return CHAT


# /now
async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message is not None
    manager: ChatManager = context.bot_data['manager']
    user = update.message.from_user
    text = plain_text(manager.get(user).prompt)
    mode = manager.get(user).mode
    await update.message.reply_text(
        context.bot_data['hint']['show'].format(mode, text), ParseMode.HTML
    )
    log(user, statics.show.format(mode))
    return CHAT


show_handler = CommandHandler('show', show)
now_handler = CommandHandler('now', now)
show_callback = CallbackQueryHandler(callback, r'[^(back)]')
