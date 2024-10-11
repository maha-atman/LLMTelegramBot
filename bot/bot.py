import os
import requests
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

TOKEN = os.getenv('TELEGRAM_TOKEN')
API_KEY = os.getenv('SAMBANOVA_API_KEY')

API_URL = "https://api.sambanova.ai/v1/chat/completions"

async def get_ai_response(message: str):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "stream": False,
        "model": "Meta-Llama-3.1-405B-Instruct",
        "messages": [{"role": "user", "content": message}]
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    return "Error processing your request. Please try again."

async def start(update: Update, context):
    welcome_messages = [
        "Greetings, intrepid explorer! I am M.A.H.A - your Multipurpose Artificial Human Assistant.",
        "Welcome to the future of assistance! I'm M.A.H.A, your Multipurpose Artificial Human Assistant.",
        "Salutations, esteemed user! M.A.H.A at your service - your very own Multipurpose Artificial Human Assistant.",
        "Hello there! M.A.H.A here, your trusted Multipurpose Artificial Human Assistant.",
        "Welcome aboard! I'm M.A.H.A, your Multipurpose Artificial Human Assistant for all things AI and beyond.",
        "Hi, I'm M.A.H.A - your Multipurpose Artificial Human Assistant, here to help you explore AI!",
        "Salutations! M.A.H.A, your Multipurpose Artificial Human Assistant, at your service!",
        "Greetings! M.A.H.A, your Multipurpose Artificial Human Assistant, is ready to push the boundaries of possibility!",
        "Welcome! I'm M.A.H.A, your Multipurpose Artificial Human Assistant, here to solve problems and explore ideas.",
        "Hello! M.A.H.A, your Multipurpose Artificial Human Assistant, reporting for duty. Let's get started!"
    ]
    await update.message.reply_text(random.choice(welcome_messages))

async def handle_message(update: Update, context):
    user_message = update.message.text
    ai_response = await get_ai_response(user_message)
    await update.message.reply_text(ai_response)

def create_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app
