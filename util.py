import json

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# status
CHAT, NEW, EDIT, SWITCH, DEL, SHOW = range(6)


def reshape(tar):
    ret = []
    for i in range(1, len(tar), 2):
        ret.append([tar[i - 1], tar[i]])
    if len(tar) % 2 == 1:
        ret.append([tar[-1]])
    return ret


def get_modes():
    with open('./config.json', 'r') as f:
        con = json.load(f)
    return list(con['prompt'].keys())


def set_mode(mode, text):
    with open('./config.json', 'r') as f:
        con = json.load(f)
        con['prompt'][mode] = text
    with open('./config.json', 'w') as f:
        json.dump(con, f, ensure_ascii=False)


def del_mode(mode):
    with open('./config.json', 'r') as f:
        con = json.load(f)
        con['prompt'].pop(mode)
    with open('./config.json', 'w') as f:
        json.dump(con, f, ensure_ascii=False)


def match(data):
    return data in get_modes()


async def choose_template(update: Update, context: ContextTypes.DEFAULT_TYPE,
                          text: str):
    button = InlineKeyboardMarkup(
        reshape([
            InlineKeyboardButton(text=key, callback_data=key)
            for key in context.bot_data['prompt']
        ] + [
            InlineKeyboardButton(text=context.bot_data['hint']['back_inline'],
                                 callback_data='back')
        ]))
    assert update.message is not None
    await update.message.reply_text(text=text, reply_markup=button)
