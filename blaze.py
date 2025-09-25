import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import openai
import asyncio

# Flask
server = Flask(__name__)

# Ключи
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет. Я Блейз. Строгий и рассудительный собеседник.")

# Ответы через OpenAI
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты строгий и рассудительный персонаж по имени Блейз."},
                {"role": "user", "content": user_message},
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Ошибка: {e}"
    await update.message.reply_text(reply)

# Создаём Application
app_telegram = Application.builder().token(TELEGRAM_TOKEN).build()
app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

# Webhook endpoint
@server.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, app_telegram.bot)
    asyncio.run(app_telegram.process_update(update))
    return "ok"

# Главная страница
@server.route("/")
def home():
    return "Блейз бот работает!"

# Устанавливаем webhook и запускаем Flask
if __name__ == "__main__":
    app_telegram.bot.set_webhook(url=f"https://blaze-1-rxpr.onrender.com/{TELEGRAM_TOKEN}")
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
