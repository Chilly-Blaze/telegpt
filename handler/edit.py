from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from util import CHAT, EDIT, choose_template, reshape, set_mode, match


async def choose_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = context.bot_data['hint']['edit_choose']
    await choose_template(update, context, text)
    return EDIT


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    assert query and query.data and query.message and context.user_data is not None
    await query.answer()
    context.user_data['edit'] = query.data
    context.user_data['del_id'] = (query.message.chat_id,
                                   query.message.message_id)
    button = InlineKeyboardMarkup(
        reshape([
            InlineKeyboardButton(text=context.bot_data['hint']['back_inline'],
                                 callback_data='back')
        ]))
    await query.edit_message_text(context.bot_data['hint']['edit'].format(
        query.data),
                                  reply_markup=button)
    return EDIT


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message is not None
    if context.user_data is None or 'edit' not in context.user_data:
        await update.message.reply_text(context.bot_data['hint']['edit_empty'])
        return 0
    mode = context.user_data['edit']
    context.user_data.pop('edit')
    text = update.message.text
    context.bot_data['prompt'][mode] = text
    set_mode(mode, text)
    await update.message.reply_text(context.bot_data['hint']['edit_complete'])
    await context.bot.delete_message(*context.user_data.pop('del_id'))
    return CHAT


edit_handler = CommandHandler('edit', choose_edit)
edit_callback = CallbackQueryHandler(callback, match)
edit_complete = MessageHandler(filters.TEXT, message)
