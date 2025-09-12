# pip install aiogram aiohttp
#from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
 


import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from secret import secrets
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import logging
from datetime import datetime

#создаст файл bot.log, куда будут записываться события.
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)


#Функция логирования
def log_action(user: types.User, button: str, api: str, answer: str):
    now = datetime.now()
    log_entry = (
        f"id={user.id}, username={user.username}, button={button}, api={api}, "
        f"date={now.strftime('%Y-%m-%d')}, time={now.strftime('%H:%M:%S')}, answer={answer}"
    )
    logging.info(log_entry)



bot = Bot(token=secrets['BOT_API_TOKEN'])
dp = Dispatcher()

#Кнопки меню
menu_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Погода в Минске", callback_data="weather")],
        [InlineKeyboardButton(text="Курс USD → BYN", callback_data="currency")],
        [InlineKeyboardButton(text="Курс биткойна", callback_data="bitcoin")]
    ]
)

#Установка командного меню
async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="start", description="Запустить бота"),
        types.BotCommand(command="weather", description="Погода в Минске"),
        types.BotCommand(command="currency", description="Курс доллара к BYN"),
        types.BotCommand(command="bitcoin", description="Курс биткойна к USD")
    ]
    await bot.set_my_commands(commands)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Выбери действие:", reply_markup=menu_inline)

#Обработчик кнопок
@dp.callback_query()
async def handle_callback(callback: CallbackQuery):
    action = callback.data

    if action == "weather":
        await get_weather(callback.message)
    elif action == "currency":
        await get_currency(callback.message)
    elif action == "bitcoin":
        await get_bitcoin(callback.message)
    else:
        await callback.message.answer("Неизвестная команда")

    await callback.answer()  #Закрывает "часики" на кнопке


#Погода
async def get_weather(message: types.Message):
    city = "Minsk"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={secrets['OPENWEATHER_API_KEY']}&units=metric&lang=ru"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if resp.status == 200:
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                humidity = data['main']['humidity']
                wind = data['wind']['speed']
                answer = (
                    f"Погода в Минске:\n"
                    f"Температура: {temp}°C\n"
                    f"Описание: {desc}\n"
                    f"Влажность: {humidity}%\n"
                    f"Ветер: {wind} м/с"
                )
                await message.answer(answer)
                #Добавляем логирование
                log_action(message.from_user, "weather", "OpenWeatherMap", answer)
            else:
                await message.answer("Не удалось получить данные о погоде")


#Курс USD → BYN
async def get_currency(message: types.Message):
    url = f"https://v6.exchangerate-api.com/v6/{secrets['EXCHANGERATE_API_KEY']}/latest/USD"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if resp.status == 200:
                byn = data['conversion_rates'].get('BYN')
                if byn:
                    answer = f"1 USD = {byn:.2f} BYN"
                    await message.answer(answer)
                    #Добавляем логирование
                    log_action(message.from_user, "currency", "ExchangeRate API", answer)
                else:
                    await message.answer("Курс BYN не найден")
            else:
                await message.answer("Не удалось получить курс валют")


#Курс Биткойна
async def get_bitcoin(message: types.Message):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if resp.status == 200 and "bitcoin" in data:
                rate = data['bitcoin']['usd']
                answer = f"1 BTC = {rate:.2f} USD"
                await message.answer(answer)
                #Добавляем логирование
                log_action(message.from_user, "bitcoin", "CoinGecko", answer)
            else:
                await message.answer("Не удалось получить курс биткойна")


# Обработчик любого текстового сообщения
@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Вы написали: '{message.text}', я не знаю такой команды")




#Запуск
async def main():
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())