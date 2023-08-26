import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from log import WARN, log, statics
import inspect

# State
CONFIG = './config.json'
HINT = './hint.json'
PROMPT = './prompt.json'
DEFAULT = 'default'
CHAT, NEW, EDIT, SWITCH, DEL, SHOW = [object() for _ in range(6)]


def read_file(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)


def write_file(content: dict, path: str) -> None:
    with open(path, 'w') as f:
        json.dump(content, f, ensure_ascii=False)


# Get config content
def get_config():
    return read_file(CONFIG)


# Get prompt content
def get_prompt(name: str | None = DEFAULT):
    return read_file(PROMPT).get(name, '')


# Add/Del prompt
def operate_prompt(key: str | None, value='', add=True):
    assert key
    content = read_file(PROMPT)
    if add:
        content[key] = value
    else:
        content.pop(key, '')
    write_file(content, PROMPT)


# Get hint content
def get_hint():
    with open('./hint.json', 'r') as f:
        return json.load(f)


# Button layout
def reshape(tar):
    ret = []
    for i in range(1, len(tar), 2):
        ret.append([tar[i - 1], tar[i]])
    if len(tar) % 2 == 1:
        ret.append([tar[-1]])
    return ret


# Authentication
def authen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    assert update.message
    user = update.message.from_user
    if user is None or str(user.id) != context.bot_data['master']:
        log(user, statics.illegal.format(inspect.stack()[1].function), WARN)
        return False
    return True


# Prompt choose button
def prompt_buttons():
    return InlineKeyboardMarkup(
        reshape(
            [
                InlineKeyboardButton(text=key, callback_data=key)
                for key in {**read_file(PROMPT), 'back': ''}
            ]
        )
    )


# Convert to plain text
def plain_text(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
