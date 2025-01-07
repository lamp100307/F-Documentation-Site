from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
def main_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text='Новые вопросы'),
            KeyboardButton(text='Отключить уведомления')
        ]
    ]
    murkup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return murkup