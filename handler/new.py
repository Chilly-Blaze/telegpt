from telegram import Message, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from log import log, statics
from util import CHAT, NEW, authen, operate_prompt


# /new (authen)
async def new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not authen(update, context):
        return CHAT
    text = context.bot_data['hint']['new_choose']
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text='back', callback_data='back')]]
    )
    assert update.message and context.chat_data is not None
    context.chat_data['last'] = await update.message.reply_text(
        text=text, reply_markup=button
    )
    return NEW


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message
    name = update.message.text
    operate_prompt(name)
    await update.message.delete()
    assert context.chat_data is not None
    msg: Message = context.chat_data['last']
    await msg.edit_text(
        context.bot_data['hint']['new'].format(name),
    )
    log(update.message.from_user, statics.new.format(name))
    return CHAT


new_handler = CommandHandler('new', new)
new_message = MessageHandler(filters.TEXT, message)
