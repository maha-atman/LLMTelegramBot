from telegram import Update
from telegram.ext import Application, CallbackQueryHandler
from fastapi import FastAPI, Request
import os
from bot import create_bot, handle_callback

app = FastAPI()

@app.post("/{token}")
async def handle_webhook(token: str, request: Request):
    bot_app = create_bot()

    if token != os.getenv('TELEGRAM_TOKEN'):
        return {"status": "Invalid token"}

    data = await request.json()
    telegram_update = Update.de_json(data, bot_app.bot)

    await bot_app.initialize()
    await bot_app.process_update(telegram_update)

    return {"status": "ok", "message": "Bot is ready!"}