from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from util import CHAT


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.callback_query
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=context.bot_data['hint']['back'])
    return CHAT


back_callback = CallbackQueryHandler(back, 'back')
