from flask import Flask, request, jsonify
import os
import telebot
import requests
import random

# Load environment variables
TOKEN = os.getenv('TELEGRAM_TOKEN')
API_KEY = os.getenv('SAMBANOVA_API_KEY')

# Initialize the Flask app
app = Flask(__name__)

# Initialize bot with your Telegram token
bot = telebot.TeleBot(TOKEN)

# SambaNova API details
API_URL = "https://api.sambanova.ai/v1/chat/completions"

@app.route(f'/{TOKEN}', methods=['POST'])  # Webhook route for Telegram
def webhook():
    json_str = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/', methods=['GET'])  # Health check route
def index():
    return jsonify({"status": "Bot is alive!"})

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
        return ai_message
    else:
        return "I'm sorry, but I encountered an error while processing your request. Please try again later."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_messages = [
        "Greetings, intrepid explorer! I am M.A.H.A - your Multipurpose Artificial Human Assistant. Prepare to embark on a journey of knowledge and discovery!",
        "Welcome to the future of assistance! I'm M.A.H.A, your Multipurpose Artificial Human Assistant. Together, we'll push the boundaries of what's possible!",
        "Salutations, esteemed user! M.A.H.A at your service - your very own Multipurpose Artificial Human Assistant. Let's make the impossible possible!",
        "Hello there! M.A.H.A here, your Multipurpose Artificial Human Assistant. Buckle up for an adventure in artificial intelligence!",
        "Welcome aboard the SS Innovation! I'm Captain M.A.H.A, your Multipurpose Artificial Human Assistant. Let's chart a course for brilliance!"
    ]
    chosen_message = random.choice(welcome_messages)
    bot.reply_to(message, chosen_message)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_message = message.text
    ai_response = get_ai_response(user_message)
    bot.reply_to(message, ai_response)

if __name__ == "__main__":
    app.run()
