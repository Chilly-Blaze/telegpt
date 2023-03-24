from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from util import CHAT


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    assert query is not None
    await query.answer()
    await query.edit_message_text(text=context.bot_data['hint']['back'])
    return CHAT


back_callback = CallbackQueryHandler(back, '^back$')
