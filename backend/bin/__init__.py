__all__ = ('API_BOT', 'logger', 'Database', 'Question', 'Answer', 'db', 'main_keyboard')

from sys import stdout, exit

from environs import *
from loguru import logger
from classes import *
from keyboards import main_keyboard

db = Database()

env = Env()

env.read_env()

try:
    API_BOT = env.str('API_BOT')
except EnvError as e:
    logger.exception(f'Переменные окружения не заданы: {e}')
    exit()

log_format = '{time:H:mm:ss} | "{function}" | {line} ({module}) | <level>{level}</level> | {message}'

logger.remove()
logger.add(
        sink=stdout,
        format=log_format,
        backtrace=True,
        diagnose=True,
        level='DEBUG',
        colorize=True
)
logger.add(
        format=log_format,
        sink='..//temp//log.log',
        level='INFO',
        mode='w',
)
