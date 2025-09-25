import os
import openai
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Flask-сервер для Render
server = Flask(__name__)

# API ключи
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # https://твой-app.onrender.com/webhook

openai.api_key = OPENAI_API_KEY

# Создаём Telegram Application
app_telegram = Application.builder().token(TELEGRAM_TOKEN).build()

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

# Регистрируем хендлеры
app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

# Flask маршрут для Telegram webhook
@server.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), app_telegram.bot)
    app_telegram.update_queue.put_nowait(update)
    return "ok", 200

# Главная страница
@server.route("/", methods=["GET"])
def home():
    return "Блейз бот работает!"

if __name__ == "__main__":
    # Устанавливаем вебхук (один раз при запуске)
    import asyncio
    async def set_webhook():
        await app_telegram.bot.set_webhook(f"{WEBHOOK_URL}/webhook")

    asyncio.get_event_loop().run_until_complete(set_webhook())

    # Запускаем Flask-сервер
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
