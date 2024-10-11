from telegram import Update
from telegram.ext import Application
from fastapi import FastAPI, Request
import os

from bot import create_bot  # Assuming create_bot function initializes the Application

app = FastAPI()

@app.post("/{token}")
async def handle_webhook(token: str, request: Request):
    bot_app = create_bot()  # Create the bot application
    
    # Ensure token is valid
    if token != os.getenv('TELEGRAM_TOKEN'):
        return {"status": "Invalid token"}

    # Load JSON data from request
    data = await request.json()
    telegram_update = Update.de_json(data, bot_app.bot)

    # Initialize the bot before processing updates
    await bot_app.initialize()

    # Process the update
    await bot_app.process_update(telegram_update)
    return {"status": "ok"}