from dotenv import load_dotenv
import os
import json
import telebot
import requests

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
API_KEY = os.getenv('SAMBANOVA_API_KEY')

# Initialize bot with your Telegram token
bot = telebot.TeleBot(TOKEN)

# SambaNova API details
API_URL = "https://api.sambanova.ai/v1/chat/completions"

def get_ai_response(message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "stream": False,
        "model": "Meta-Llama-3.1-405B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        ai_message = result['choices'][0]['message']['content']
        return ai_message  # Directly return the AI message
    else:
        return "I'm sorry, but I encountered an error while processing your request. Please try again later."

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_message = message.text
    ai_response = get_ai_response(user_message)
    bot.reply_to(message, ai_response)

# Start polling
if __name__ == "__main__":
    bot.polling()
