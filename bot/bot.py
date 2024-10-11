import os
import random
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler

TOKEN = os.getenv('TELEGRAM_TOKEN')

MAX_MESSAGE_LENGTH = 4000
conversation_history = {}

# Define AI providers and their models
AI_PROVIDERS = {
    'OpenAI': ['gpt-4o-mini'],
    'Groq': ['llama-3.1-70b-versatile'],
    'Together': ['meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo'],
    'Google': ['gemini-1.5-flash-002'],
    'Claude': ['claude-3-5-sonnet-20240620'],
    'Hyperbolic': ['NousResearch/Hermes-3-Llama-3.1-70B'],
    'Mistral': ['mistral-large-latest'],
    'Cerebras': ['llama3.1-70b'],
    'SambaNova': ['Meta-Llama-3.1-405B-Instruct']
}

# Default provider and model
DEFAULT_PROVIDER = 'SambaNova'
DEFAULT_MODEL = 'Meta-Llama-3.1-405B-Instruct'

# Store user preferences
user_preferences = {}

system_message = {
    "role": "system",
    "content": """You are M.A.H.A. (Multipurpose Artificial Human Assistant), an advanced AI with sophisticated reasoning capabilities. Approach all interactions with friendly enthusiasm and intellectual rigor."""
}

def truncate_message(message: str) -> str:
    if len(message) <= MAX_MESSAGE_LENGTH:
        return message
    return message[:MAX_MESSAGE_LENGTH - 3] + "..."

def format_key_name(provider: str) -> str:
    return f"{provider.upper()}_API_KEY"

async def current_ai(update: Update, context):
    user_id = update.effective_user.id
    provider = user_preferences.get(user_id, {}).get('provider', DEFAULT_PROVIDER)
    model = user_preferences.get(user_id, {}).get('model', DEFAULT_MODEL)
    await update.message.reply_text(f"Current AI Provider: {provider}\nCurrent Model: {model}")

async def list_models(update: Update, context):
    message = "Available AI Providers and Models:\n\n"
    for provider, models in AI_PROVIDERS.items():
        message += f"{provider}:\n"
        for model in models:
            message += f"  - {model}\n"
    await update.message.reply_text(message)

async def clear_chat(update: Update, context):
    user_id = update.effective_user.id
    if user_id in conversation_history:
        conversation_history[user_id] = []
        await update.message.reply_text("Your conversation history has been cleared.")
    else:
        await update.message.reply_text("You don't have any conversation history to clear.")

async def help_command(update: Update, context):
    help_text = (
        "Here are the available commands:\n\n"
        "/start - Display the welcome message\n"
        "/settings - Change AI provider and model\n"
        "/current_ai - Check current AI provider and model\n"
        "/list_models - List all available AI providers and models\n"
        "/clear_chat - Clear your conversation history\n"
        "/help - Display this help message\n\n"
        "You can also just type your message to chat with the AI directly."
    )
    await update.message.reply_text(help_text)

async def get_ai_response(message: str, user_id: int):
    global conversation_history
    provider = user_preferences.get(user_id, {}).get('provider', DEFAULT_PROVIDER)
    model = user_preferences.get(user_id, {}).get('model', DEFAULT_MODEL)

    api_key = os.getenv(format_key_name(provider))
    if not api_key:
        return f"{provider} API key not found. Please set the API key in the environment variables."

    headers = {
        "Content-Type": "application/json"
    }
    
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    conversation_history[user_id].append({"role": "user", "content": message})

    if provider == 'OpenAI':
        API_URL = "https://api.openai.com/v1/chat/completions"
        headers["Authorization"] = f"Bearer {api_key}"
        data = {
            "model": model,
            "messages": [system_message] + conversation_history,
            "temperature": 0.7
        }
    elif provider == 'Groq':
        API_URL = "https://api.groq.com/openai/v1/chat/completions"
        headers["Authorization"] = f"Bearer {api_key}"
        data = {
            "model": model,
            "messages": [system_message] + conversation_history,
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 0.9,
            "stream": False
        }
    elif provider == 'Together':
        API_URL = "https://api.together.ai/chat/completions"
        headers["Authorization"] = f"Bearer {api_key}"
        data = {
            "model": model,
            "messages": [system_message] + conversation_history,
            "max_tokens": 2048,
            "temperature": 0.7,
            "top_p": 0.8,
            "stop": []
        }
    elif provider == 'Google':
        API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        data = {
            "contents": [{"role": msg["role"], "parts": [{"text": msg["content"]}]} for msg in [system_message] + conversation_history],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192
            }
        }
    elif provider == 'Claude':
        API_URL = "https://api.anthropic.com/v1/messages"
        headers["x-api-key"] = api_key
        headers["anthropic-version"] = "2023-06-01"
        data = {
            "model": model,
            "max_tokens": 2048,
            "temperature": 0.7,
            "messages": [system_message] + conversation_history
        }
    elif provider == 'Hyperbolic':
        API_URL = "https://api.hyperbolic.xyz/v1/chat/completions"
        headers["Authorization"] = f"Bearer {api_key}"
        data = {
            "messages": [system_message] + conversation_history,
            "model": model,
            "max_tokens": 2048,
            "temperature": 0.7,
            "top_p": 0.9,
            "stream": False
        }
    elif provider == 'Mistral':
        API_URL = "https://api.mistral.ai/v1/chat/completions"
        headers["Authorization"] = f"Bearer {api_key}"
        data = {
            "model": model,
            "messages": [system_message] + conversation_history,
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 1,
            "stream": False,
            "safe_prompt": False
        }
    elif provider == 'Cerebras':
        API_URL = "https://api.cerebras.ai/v1/chat/completions"
        headers["Authorization"] = f"Bearer {api_key}"
        data = {
            "model": model,
            "messages": [system_message] + conversation_history,
            "temperature": 0.7,
            "max_tokens": -1,
            "seed": 0,
            "top_p": 1,
            "stream": False
        }
    elif provider == 'SambaNova':
        API_URL = "https://api.sambanova.ai/v1/chat/completions"
        headers["Authorization"] = f"Bearer {api_key}"
        data = {
            "model": model,
            "messages": [system_message] + conversation_history,
            "temperature": 0.7,
            "stream": False
        }
    else:
        return "Invalid AI provider selected."

    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if provider == 'Google':
            ai_message = result['candidates'][0]['content']['parts'][0]['text']
        elif provider == 'Claude':
            ai_message = result['content'][0]['text']
        else:
            ai_message = result['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": ai_message})
        return ai_message
    return f"Error processing your request. Status code: {response.status_code}"

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

async def start(update: Update, context):
    welcome_message = random.choice(welcome_messages)
    command_info = (
        "\n\nHere are the available commands:\n\n"
        "/settings - Change AI provider and model\n"
        "/current_ai - Check current AI provider and model\n"
        "/list_models - List all available AI providers and models\n"
        "/clear_chat - Clear your conversation history\n"
        "/help - Display this help message\n\n"
        "You can start chatting with me directly by typing your message. "
        "The default AI provider is set to SambaNova with the Meta-Llama-3.1-405B-Instruct model."
    )
    full_message = welcome_message + command_info
    await update.message.reply_text(full_message)

async def show_provider_selection(update: Update, context):
    keyboard = [[InlineKeyboardButton(provider, callback_data=f"provider_{provider}") for provider in AI_PROVIDERS.keys()]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please select an AI provider:', reply_markup=reply_markup)

async def show_model_selection(update: Update, context, provider):
    keyboard = [[InlineKeyboardButton(model, callback_data=f"model_{provider}_{model}") for model in AI_PROVIDERS[provider]]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text(f'Please select a model for {provider}:', reply_markup=reply_markup)

async def handle_callback(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = update.effective_user.id
    
    if data.startswith('provider_'):
        provider = data.split('_')[1]
        user_preferences[user_id] = {'provider': provider}
        await show_model_selection(update, context, provider)
    elif data.startswith('model_'):
        _, provider, model = data.split('_', 2)
        user_preferences[user_id] = {'provider': provider, 'model': model}
        await query.message.edit_text(f'You have selected {provider} with model {model}. You can now start chatting!')

async def handle_message(update: Update, context):
    user_message = update.message.text
    user_id = update.effective_user.id
    
    if user_id not in user_preferences:
        user_preferences[user_id] = {'provider': DEFAULT_PROVIDER, 'model': DEFAULT_MODEL}
    
    ai_response = await get_ai_response(user_message, user_id)
    
    if len(ai_response) > MAX_MESSAGE_LENGTH:
        for i in range(0, len(ai_response), MAX_MESSAGE_LENGTH):
            chunk = ai_response[i:i + MAX_MESSAGE_LENGTH]
            await update.message.reply_text(chunk)
    else:
        await update.message.reply_text(ai_response)

def create_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('settings', show_provider_selection))
    app.add_handler(CommandHandler('current_ai', current_ai))
    app.add_handler(CommandHandler('list_models', list_models))
    app.add_handler(CommandHandler('clear_chat', clear_chat))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app