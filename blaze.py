import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import openai
from flask import Flask
import threading

# Flask для Render
server = Flask(__name__)

@server.route("/")
def home():
    return "Блейз бот работает!"

# Telegram/OpenAI ключи из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет. Я Блейз. Строгий и рассудительный собеседник.")

# Обработка сообщений
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

# Основная функция
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Блейз запущен")
    app.run_polling()

# Запуск Telegram + Flask
if __name__ == "__main__":
    threading.Thread(target=main).start()
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
