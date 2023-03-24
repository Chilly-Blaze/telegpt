from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler
from util import choose_template, CHAT, SWITCH, match


async def choose_switch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = context.bot_data['hint']['switch_choose'].format(
        context.bot_data['mode'])
    await choose_template(update, context, text)
    return SWITCH


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    assert query is not None
    await query.answer()
    if context.bot_data['mode'] == query.data:
        await query.edit_message_text(
            text=context.bot_data['hint']['switch_equal'].format(query.data))
    else:
        context.bot_data['mode'] = query.data
        context.bot_data['chat'].reset(
            system_prompt=context.bot_data['prompt'][query.data])
        await query.edit_message_text(
            text=context.bot_data['hint']['switch_succ'].format(query.data))
    return CHAT


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.bot_data['mode']
    context.bot_data['chat'].reset(
        system_prompt=context.bot_data['prompt'][mode])
    assert update.message is not None
    await update.message.reply_text(text=context.bot_data['hint']['reset'])
    return CHAT


reset_handler = CommandHandler('reset', reset)
switch_handler = CommandHandler('switch', choose_switch)
switch_callback = CallbackQueryHandler(callback, match)
