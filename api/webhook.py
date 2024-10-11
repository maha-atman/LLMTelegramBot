from telegram import Update
from telegram.ext import Application
from fastapi import FastAPI, Request, HTTPException
import os

from bot import create_bot  # Function that initializes the Application

app = FastAPI()

# Initialize the bot application once
bot_app = create_bot() 

@app.post("/{token}")
async def handle_webhook(token: str, request: Request):
    # Ensure token is valid
    if token != os.getenv('TELEGRAM_TOKEN'):
        raise HTTPException(status_code=403, detail="Invalid token")

    # Load JSON data from request
    data = await request.json()
    telegram_update = Update.de_json(data, bot_app.bot)

    # Process the update
    try:
        await bot_app.process_update(telegram_update)
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    return {"status": "ok"}
