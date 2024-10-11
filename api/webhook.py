import os
from telegram import Update
from telegram.ext import Application
from bot import create_bot

TOKEN = os.getenv('TELEGRAM_TOKEN')

def main():
    app = create_bot()

    # Vercel automatically provides the deployment URL
    vercel_url = os.getenv('VERCEL_URL')

    # Configure the bot's webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", "3000")),
        url_path=TOKEN,
        webhook_url=f"https://{vercel_url}/{TOKEN}"
    )

if __name__ == "__main__":
    main()