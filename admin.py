import schedule
import telebot
from threading import Thread
from time import sleep

TOKEN = "Some Token"

bot = telebot.TeleBot(TOKEN)
some_id = 12345 # This is our chat id.

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

def function_to_run():
    return bot.send_message(some_id, "This is a message to send.")

if __name__ == "__main__":
    # Create the job in schedule.
    schedule.every().saturday.at("07:00").do(function_to_run)

    # Spin up a thread to run the schedule check so it doesn't block your bot.
    # This will take the function schedule_checker which will check every second
    # to see if the scheduled job needs to be ran.
    Thread(target=schedule_checker).start() 

    # And then of course, start your server.
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))



    import telebot
import config
from datetime import time, date, datetime

bot = telebot.TeleBot(config.bot_token)
chat_id=config.my_id    

@bot.message_handler(commands=['start', 'help'])
def print_hi(message):
    bot.send_message(message.chat.id, 'Hi!')


@bot.message_handler(func=lambda message: False) #cause there is no message
def saturday_message():
    now = datetime.now()
    if (now.date().weekday() == 5) and (now.time() == time(8,0)):
        bot.send_message(chat_id, 'Wake up!')

bot.polling(none_stop=True)





#Запланированное ежедневное сообщение
# рандомный выбор user id 
# Антибот
# Анти спам ( user jnghfdkztn > 10 соб мин) 