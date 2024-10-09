# webhook.py
from flask import Flask, request, jsonify
from bot.bot import bot, TOKEN, get_ai_response  # Import get_ai_response

app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])  # Webhook for Telegram
def webhook():
    json_str = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/', methods=['GET'])  # Health check route
def index():
    return jsonify({"status": "Bot is alive!"})

@app.route('/api/send_message', methods=['POST'])  # Endpoint for sending messages
def send_message():
    data = request.get_json()
    user_message = data.get('message')
    ai_response = get_ai_response(user_message)  # Call the imported function
    return jsonify({"reply": ai_response})

if __name__ == "__main__":
    app.run(debug=True)
