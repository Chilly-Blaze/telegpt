from telegram import Message, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from log import log, statics
from util import CHAT, EDIT, authen, get_prompt, operate_prompt, plain_text, prompt_buttons, reshape
from telegram.constants import ParseMode


# /edit (authen)
async def edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not authen(update, context):
        return CHAT
    assert update.message
    text = context.bot_data['hint']['edit_choose']
    assert context.chat_data is not None
    context.chat_data['last'] = await update.message.reply_text(
        text, reply_markup=prompt_buttons()
    )
    return EDIT


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    assert query and query.data is not None
    await query.answer()
    assert context.chat_data is not None
    context.chat_data['edit'] = query.data
    button = InlineKeyboardMarkup(
        reshape([InlineKeyboardButton(text='back', callback_data='back')])
    )
    await query.edit_message_text(
        context.bot_data['hint']['edit'].format(
            query.data, plain_text(get_prompt(query.data))
        ),
        reply_markup=button,
        parse_mode=ParseMode.HTML,
    )
    return EDIT


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message and context.chat_data is not None
    msg: Message = context.chat_data['last']
    if 'edit' not in context.chat_data:
        await msg.edit_text(
            context.bot_data['hint']['edit_empty'], reply_markup=prompt_buttons()
        )
        await update.message.delete()
        return EDIT
    mode = context.chat_data.pop('edit')
    text = update.message.text
    old_text = get_prompt(mode)
    operate_prompt(mode, '' if text is None else text)
    await update.message.delete()
    await msg.edit_text(context.bot_data['hint']['edit_complete'])
    log(update.message.from_user, statics.edit.format(old_text, text))
    return CHAT


edit_handler = CommandHandler('edit', edit)
edit_callback = CallbackQueryHandler(callback, r'[^(back)]')
edit_complete = MessageHandler(filters.TEXT, message)
