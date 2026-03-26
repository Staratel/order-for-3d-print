import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import os
from loguru import logger

CHAT_ID = os.environ.get("CHAT_ID")

def get_external_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except Exception as e:
        logger.info(e)

async def on_startup(app):
    ip = get_external_ip()
    logger.info(f"Startup watchdog. {CHAT_ID=}, {ip=}")
    await app.bot.send_message(
        chat_id=CHAT_ID, text=ip
    )
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"chat_id: {update.message.chat_id}")
    logger.info(update.message)
    if update.message and update.message.chat_id == CHAT_ID:
        await update.message.reply_text(update.message.text)

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get("TOKEN","")).post_init(on_startup).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


    logger.info("Bot started")
    app.run_polling()