from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler
from chatapi import ChatManager
from log import log, statics
from util import prompt_buttons, CHAT, SWITCH


# /switch
async def switch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message
    manager: ChatManager = context.bot_data['manager']
    user = update.message.from_user
    text = context.bot_data['hint']['switch_choose'].format(manager.get(user).mode)
    await update.message.reply_text(
        text, reply_markup=prompt_buttons(), parse_mode=ParseMode.HTML
    )
    return SWITCH


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.callback_query
    query = update.callback_query
    manager: ChatManager = context.bot_data['manager']
    user = query.from_user
    mode = manager.get(user).mode
    await query.answer()
    if mode == query.data:
        await query.edit_message_text(
            text=context.bot_data['hint']['switch_equal'].format(query.data),
            parse_mode=ParseMode.HTML,
        )
    else:
        manager.new(user, query.data)
        await query.edit_message_text(
            text=context.bot_data['hint']['switch_succ'].format(query.data),
            parse_mode=ParseMode.HTML,
        )
        log(user, statics.switch.format(mode, query.data))
    return CHAT


# /reset
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message is not None
    user = update.message.from_user
    manager: ChatManager = context.bot_data['manager']
    manager.new(user, manager.get(user).mode)
    await update.message.reply_text(text=context.bot_data['hint']['reset'])
    log(user, statics.reset.format(manager.get(user).mode))
    return CHAT


reset_handler = CommandHandler('reset', reset)
switch_handler = CommandHandler('switch', switch)
switch_callback = CallbackQueryHandler(callback, r'[^(back)]')
