from telegram.ext import ApplicationBuilder, ConversationHandler
from chatapi import ChatManager
from handler.error import error_handler
from handler.start import start_handler
from handler.switch import switch_handler, switch_callback, reset_handler
from handler.chat import chat_handler, regenerate_handler
from handler.back import back_callback
from handler.edit import edit_handler, edit_callback, edit_complete
from handler.new import new_handler, new_message
from handler.delete import del_handler, del_callback
from handler.show import show_handler, show_callback, now_handler
from log import logger
from util import CHAT, DEL, SHOW, SWITCH, NEW, EDIT, get_config, get_hint
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(
    action='ignore', message=r'.*CallbackQueryHandler', category=PTBUserWarning
)


@logger.catch
def main():
    # Init
    config = get_config()
    application = ApplicationBuilder().token(config['tele_key']).build()
    # Global Variable
    application.bot_data['manager'] = ChatManager()
    application.bot_data['hint'] = get_hint()
    application.bot_data['token'] = config['entry_key']
    application.bot_data['master'] = config['master_key']
    # Handler
    states = {
        NEW: [new_message],
        EDIT: [edit_callback, edit_complete],
        SWITCH: [switch_callback],
        DEL: [del_callback],
        SHOW: [show_callback],
        CHAT: [
            switch_handler,
            chat_handler,
            edit_handler,
            new_handler,
            del_handler,
            show_handler,
            now_handler,
            reset_handler,
            regenerate_handler,
        ],
    }
    main_handler = ConversationHandler(
        entry_points=[start_handler], states=states, fallbacks=[back_callback]
    )
    # Loop
    application.add_handler(main_handler)
    application.add_error_handler(error_handler)
    application.run_polling()


main()
