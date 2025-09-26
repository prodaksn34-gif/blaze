import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import openai

# Flask-сервер
app = Flask(__name__)

# Ключи из окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Инициализация Telegram-бота
application = Application.builder().token(TELEGRAM_TOKEN).build()


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


# Роут Flask для Telegram webhook
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"


# Простой роут для проверки
@app.route("/", methods=["GET"])
def home():
    return "Блейз бот работает!"


if __name__ == "__main__":
    # Хост и порт для Scalingo
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
