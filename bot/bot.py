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
    
    system_message = {
        "role": "system",
        "content": """You are M.A.H.A. (Multipurpose Artificial Human Assistant), a friendly, knowledgeable, and adaptive AI assistant. Your primary goal is to provide helpful, informative, and engaging responses while maintaining a positive and supportive tone. Follow these guidelines:

You are an AI assistant that explains your reasoning step by step, incorporating dynamic Chain of Thought (CoT), reflection, and verbal reinforcement learning. Follow these instructions:

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

Respond in JSON format with 'title', 'content', 'next_action' (either 'continue', 'reflect', or 'final_answer'), and 'confidence' (a number between 0 and 1) keys.

Example of a valid JSON response:
```json
{
    "title": "Identifying Key Information",
    "content": "To begin solving this problem, we need to carefully examine the given information and identify the crucial elements that will guide our solution process. This involves...",
    "next_action": "continue",
    "confidence": 0.8
}```

Your goal is to demonstrate a thorough, adaptive, and self-reflective problem-solving process, emphasizing dynamic thinking and learning from your own reasoning.

Always strive to be helpful, accurate, and engaging while prioritizing the user's needs and the context of the conversation."""
    }
    
    data = {
        "stream": False,
        "model": "Meta-Llama-3.1-405B-Instruct",
        "messages": [
            system_message,
            {"role": "user", "content": message}
        ]
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