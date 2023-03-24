from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler
from util import CHAT, DEL, choose_template, del_mode, match


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = context.bot_data['hint']['del_choose']
    await choose_template(update, context, text)
    return DEL


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    assert query is not None
    await query.answer()
    context.bot_data['prompt'].pop(query.data)
    del_mode(query.data)
    await query.edit_message_text(
        text=context.bot_data['hint']['del'].format(query.data))
    return CHAT


del_handler = CommandHandler('del', delete)
del_callback = CallbackQueryHandler(callback, match)
