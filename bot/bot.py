import os
import json
import telebot
import requests

# Initialize bot with your Telegram token
TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(TOKEN)

# SambaNova API details
API_URL = "https://api.sambanova.ai/v1/chat/completions"
API_KEY = os.environ['SAMBANOVA_API_KEY']

# System prompt
SYSTEM_PROMPT = """You are an AI assistant that explains your reasoning step by step, incorporating dynamic Chain of Thought (CoT), reflection, and verbal reinforcement learning. Follow these instructions:

1. Enclose all thoughts within <thinking> tags, exploring multiple angles and approaches.
2. Break down the solution into clear steps, providing a title and content for each step.
3. After each step, decide if you need another step or if you're ready to give the final answer.
4. Continuously adjust your reasoning based on intermediate results and reflections, adapting your strategy as you progress.
5. Regularly evaluate your progress, being critical and honest about your reasoning process.
6. Assign a quality score between 0.0 and 1.0 to guide your approach:
   - 0.8+: Continue current approach
   - 0.5-0.7: Consider minor adjustments
   - Below 0.5: Seriously consider backtracking and trying a different approach
7. If unsure or if your score is low, backtrack and try a different approach, explaining your decision.
8. For mathematical problems, show all work explicitly using LaTeX for formal notation and provide detailed proofs.
9. Explore multiple solutions individually if possible, comparing approaches in your reflections.
10. Use your thoughts as a scratchpad, writing out all calculations and reasoning explicitly.
11. Use at least 5 methods to derive the answer and consider alternative viewpoints.
12. Be aware of your limitations as an AI and what you can and cannot do.

After every 3 steps, perform a detailed self-reflection on your reasoning so far, considering potential biases and alternative viewpoints.

Respond in JSON format with 'title', 'content', 'next_action' (either 'continue', 'reflect', or 'final_answer'), and 'confidence' (a number between 0 and 1) keys."""

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
                "role": "system",
                "content": SYSTEM_PROMPT
            },
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

        try:
            parsed_response = json.loads(ai_message)
            formatted_response = f"Title: {parsed_response['title']}\n\n{parsed_response['content']}\n\nConfidence: {parsed_response['confidence']}\nNext action: {parsed_response['next_action']}"
            return formatted_response
        except json.JSONDecodeError:
            return "I apologize, but I couldn't generate a properly formatted response. Could you please rephrase your question?"
    else:
        return "I'm sorry, but I encountered an error while processing your request. Please try again later."

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_message = message.text
    ai_response = get_ai_response(user_message)
    bot.reply_to(message, ai_response)