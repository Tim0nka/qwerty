import random
import time
from collections import defaultdict
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters,ContextTypes, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler

#Хранилище активности
activity_log = defaultdict(list)

def too_many_messages(user_id):
    now = time.time()
    recent = [t for t in activity_log[user_id] if now - t < 60]
    recent.append(now)
    activity_log[user_id] = recent
    return len(recent) > 10

async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = update.message.from_user
    if sender.is_bot:
        return
    if too_many_messages(sender.id):
        return
    name = sender.username or sender.first_name
    await update.message.reply_text(f"Сообщение от @{name} получено.")

async def send_daily_pick(context: CallbackContext):
    chat_id = context.job.chat_id
    bot = context.bot
    admins = await bot.get_chat_administrators(chat_id)
    people = [admin.user.id for admin in admins if not admin.user.is_bot]

    if not people:
        await bot.send_message(chat_id, "Никого не удалось выбрать.")
        return

    chosen = random.choice(people)
    await bot.send_message(chat_id, f"Сегодня выбран участник: ID {chosen}")

def run_bot():
    bot_token = "BOT_API_TOKEN"
    group_id = -3290089021821 

    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_group_message))

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        lambda: app.job_queue.run_once(send_daily_pick, when=0, chat_id=group_id),
        trigger='cron', hour=9, minute=0
    )
    scheduler.start()

    app.run_polling()

if __name__ == "__main__":
    run_bot()
