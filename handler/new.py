from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from util import CHAT, NEW, reshape, set_mode


async def new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = context.bot_data['hint']['new_choose']
    button = InlineKeyboardMarkup(
        reshape([
            InlineKeyboardButton(text=context.bot_data['hint']['back_inline'],
                                 callback_data='back')
        ]))
    assert update.message and context.user_data is not None
    msg = await update.message.reply_text(text=text, reply_markup=button)
    context.user_data['del_id'] = (msg.chat_id, msg.message_id)
    return NEW


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message and context.user_data is not None
    if update.message.text is None or len(update.message.text) > 10:
        await update.message.reply_text(
            text=context.bot_data['hint']['new_error'])
        return NEW
    context.bot_data['prompt'][update.message.text] = ''
    set_mode(update.message.text, '')
    await update.message.reply_text(context.bot_data['hint']['new'].format(
        update.message.text))
    await context.bot.delete_message(*context.user_data.pop('del_id'))
    return CHAT


new_handler = CommandHandler('new', new)
new_message = MessageHandler(filters.TEXT, message)
