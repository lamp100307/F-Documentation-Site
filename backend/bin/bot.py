__all__ = ('send_question', 'run_bot')

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from bin import API_BOT, db, main_keyboard, logger

bot = Bot(API_BOT)
dp = Dispatcher()

@dp.message(F.text, Command("start"))
async def start(message: types.Message):
    await message.answer(
            f"Привет {message.from_user.username}\nТеперь ты будешь получать новые вопросы с сайта!",
            reply_markup=main_keyboard()
    )
    await db.add_user(id_=message.from_user.id, send=True)
    logger.info(f'Пользователь {message.from_user.username} добавлен!')
    return

async def accumulation_questions():
    db.increase_counter()
    for user in db.users:
        if user['send'] is True:
            await bot.send_message(user['id'], f"У вас {user['counter']} непрочитанных вопросов")
    return

async def send_question(name, question):
    for user in await db.users:
        await bot.send_message(user['id'], f"{name}:\n{question}")
    return

async def run_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        print("Bot started")
        await dp.start_polling(bot)
    finally:
        await bot.close()