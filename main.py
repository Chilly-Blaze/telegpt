import json
from revChatGPT.V3 import Chatbot
from telegram.ext import ApplicationBuilder, ConversationHandler
from handler.start import start_handler
from handler.switch import switch_handler, switch_callback, reset_handler
from handler.chat import chat_handler
from handler.back import back_callback
from handler.edit import edit_handler, edit_callback, edit_complete
from handler.new import new_handler, new_message
from handler.delete import del_handler, del_callback
from handler.show import show_handler, show_callback, now_handler
from util import CHAT, DEL, SHOW, SWITCH, NEW, EDIT
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore",
               message=r".*CallbackQueryHandler",
               category=PTBUserWarning)

# load Config
with open('./config.json', 'r') as f:
    config = json.load(f)
with open('./hint.json', 'r') as f:
    hint = json.load(open('./hint.json'))


def main():
    # Init
    application = ApplicationBuilder().token(config['tele_api']).build()
    # Global Variable
    application.bot_data['chat'] = Chatbot(api_key=config['chat_api'])
    if 'assistant' in config['prompt']:
        application.bot_data['chat'].reset(
            system_prompt=config['prompt']['assistant'])
        application.bot_data['mode'] = 'assistant'
    else:
        application.bot_data['mode'] = 'none'
    application.bot_data['hint'] = hint
    application.bot_data['prompt'] = config['prompt']
    # Handler
    states = {
        NEW: [new_message],
        EDIT: [edit_callback, edit_complete],
        SWITCH: [switch_callback],
        DEL: [del_callback],
        SHOW: [show_callback],
        CHAT: [
            switch_handler, chat_handler, edit_handler, new_handler,
            del_handler, show_handler, now_handler, reset_handler
        ],
    }
    main_handler = ConversationHandler(entry_points=[start_handler],
                                       states=states,
                                       fallbacks=[back_callback])
    # Loop
    application.add_handler(main_handler)
    application.run_polling()


main()
