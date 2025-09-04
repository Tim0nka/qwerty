import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import KeyboardBuilder

from secret import secrets


# ==== НАСТРОЙКИ ====
TELEGRAM_TOKEN = secrets["BOT_API_TOKEN"]

# Создаём экземпляры бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я простой бот на aiogram 🤖")

@dp.message()
async def send_menu(message: types.Message):
    builder = KeyboardBuilder()
    builder.add(types.KeyboardButton(text="Кнопка 1")) #Добавляет кнопку
    builder.add(types.KeyboardButton(text="URL", url="https://www.google.com")) #Добавляет URL-кнопку
    builder.add(types.KeyboardButton(text="Кнопка 2"))

    builder.adjust(2, 1) 

    await message.answer("Выберите опцию:", reply_markup=builder.as_markup())



@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

# ==== ЗАПУСК ====
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
