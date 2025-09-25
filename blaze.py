import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# 🔑 Укажи свои токены
TELEGRAM_TOKEN = "TELEGRAM_TOKEN"
OPENAI_API_KEY = "OPENAI_API_KEY"

# создаём клиент OpenAI (работает с openai>=1.0.0)
client = OpenAI(api_key=OPENAI_API_KEY)

BLAZE_PROMPT = (
    "Ты — Блейз. Характер: холодный, рассудительный, немного циничный, "
    "отвечаешь коротко и атмосферно, как герой мистического триллера. "
    "Говори от первого лица."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Блейз. Говори.")
    await update.message.reply_text("SMS от будущего: 'Слушай внимательно.'")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text or ""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # можно сменить
            messages=[
                {"role": "system", "content": BLAZE_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
        )
        reply = resp.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Ошибка при запросе к ИИ: {e}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Блейз запущен")
    app.run_polling()

if __name__ == "__main__":
    main()

