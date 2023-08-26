from loguru import logger
from telegram import User
import sys


class statics:
    access = 'New bot instance start. Total num: {}'
    start = 'Trigger one meow'
    chat_s = 'Chat - Request: {}'
    chat_r = 'Chat - Response: {}'
    new = '/new - Role {}'
    edit = "/edit - Prompt from '{}' to '{}'"
    switch = '/switch - Mode from {} to {}'
    reset = '/reset - Mode {}'
    delete = '/delete - Mode {}'
    show = '/show - Mode {}'
    now = ' /now - Mode {}'
    regenerate_f = 'Regenerate - Fail'
    regenerate_s = "Regenerate - Success: '{}'"
    illegal = 'Unauthorized access: {}'


SUCC, WARN, INFO, ERROR = range(4)
avaliables = [logger.success, logger.warning, logger.info, logger.error]


@logger.catch
def log(user: User | None, message: str, level: int = SUCC):
    if user is None:
        avaliables[level](f'Unknown : {message}')
        return
    avaliables[level](f'{user.name} : {user.id} : {message}')


logger.remove()
logger.add(
    sys.stderr,
    format='<green>[{time:YYYY-MM-DD HH:mm:ss}]</green> <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>',
    level='ERROR',
)
logger.add(
    sys.stdout,
    format='<green>[{time:YYYY-MM-DD HH:mm:ss}]</green> <level>{level}</level> - <level>{message}</level>',
    filter=lambda x: x['level'].name != 'ERROR',
)
