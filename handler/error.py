import traceback
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from log import logger


@logger.catch
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert context.error
    info = update.to_dict() if isinstance(update, Update) else str(update)
    message = context.bot_data['hint']['runtime_error'].format(
        info, str(context.error), traceback.format_tb(context.error.__traceback__)[-1]
    )
    await context.bot.send_message(
        chat_id=context.bot_data['master'],
        text=message,
        parse_mode=ParseMode.HTML,
    )
    raise context.error
