import os
from telegram import Update
from telegram.ext import Application
from bot import create_bot
from fastapi import FastAPI

TOKEN = os.getenv('TELEGRAM_TOKEN')

# Initialize FastAPI to handle webhook requests
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    bot_app = create_bot()
    vercel_url = os.getenv('VERCEL_URL')
    
    # Configure webhook URL for the Telegram bot
    await bot_app.bot.set_webhook(f"https://{vercel_url}/{TOKEN}")

@app.post(f"/{TOKEN}")
async def handle_webhook(update: dict):
    bot_app = create_bot()
    telegram_update = Update.de_json(update, bot_app.bot)
    await bot_app.process_update(telegram_update)
    return {"status": "ok"}
