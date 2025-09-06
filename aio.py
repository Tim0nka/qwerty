import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram import F

from secret import secrets


# ==== НАСТРОЙКИ ====
TELEGRAM_TOKEN = secrets['BOT_API_TOKEN']

# Создаём экземпляры бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я простой бот на aiogram 🤖")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сказать привет 👋", callback_data="hello")],
        [InlineKeyboardButton(text="Показать смайлик 😄", callback_data="show_smile")],
        [InlineKeyboardButton(text="Показать видео 🎬", callback_data="show_video")],
        [InlineKeyboardButton(text="Перейти на сайт 🌐", url="https://example.com")]
    ])
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=keyboard)

@dp.callback_query(F.data == "show_smile")
async def send_smile(callback: types.CallbackQuery):
    await callback.answer()  # ← обязательно!
    await callback.message.answer_photo(
        photo="https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Smiley_face.png/600px-Smiley_face.png",
        caption="Вот твой смайлик! 😄"
    )

@dp.callback_query(F.data == "show_image")
async def send_image(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer_photo(
        photo="https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Smiley_face.png/600px-Smiley_face.png",
        caption="Вот твой смайлик! 😄"
    )

@dp.callback_query(F.data == "show_video")
async def send_video(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer_video(
        video="https://filesamples.com/samples/video/mp4/sample_640x360.mp4",
        caption="Вот видео в формате MP4 🎬"
    )

# Обработчик любого текстового сообщения
@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

# ==== ЗАПУСК ====
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
