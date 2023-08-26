from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler
from log import log, statics
from util import CHAT, DEL, authen, operate_prompt, prompt_buttons


# /delete (authen)
async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message
    if not authen(update, context):
        return CHAT
    text = context.bot_data['hint']['del_choose']
    await update.message.reply_text(text, reply_markup=prompt_buttons())
    return DEL


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.callback_query
    query = update.callback_query
    await query.answer()
    operate_prompt(query.data, add=False)
    await query.edit_message_text(
        text=context.bot_data['hint']['del'].format(query.data)
    )
    log(query.from_user, statics.delete.format(query.data))
    return CHAT


del_handler = CommandHandler('del', delete)
del_callback = CallbackQueryHandler(callback, r'[^(back)]')
