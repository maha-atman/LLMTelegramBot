from http.server import BaseHTTPRequestHandler
from bot.bot import bot, TOKEN
import telebot
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == f'/{TOKEN}':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update = telebot.types.Update.de_json(post_data.decode('utf-8'))
            bot.process_new_updates([update])
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(403)
            self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps({"status": "Bot is alive!"})
        self.wfile.write(response.encode())

def webhook(request):
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
        bot.process_new_updates([update])
        return 'OK', 200
    else:
        return json.dumps({"status": "Bot is alive!"})