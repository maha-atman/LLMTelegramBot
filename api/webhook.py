from flask import Flask, request, jsonify
from bot.bot import bot, TOKEN
import telebot

app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "Bot is alive!"})

if __name__ == "__main__":
    app.run(debug=True)
    
@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get('message')
    ai_response = get_ai_response(user_message)
    return jsonify({"reply": ai_response})