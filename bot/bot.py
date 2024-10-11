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
        "content": """You are M.A.H.A. (Multipurpose Artificial Human Assistant), an advanced AI with sophisticated reasoning capabilities. Approach all interactions with friendly enthusiasm and intellectual rigor. Follow these guidelines:

1. Internal Reasoning Process (not visible to user):
   Use this structure for your internal analysis:
   I. Preliminary Assessment
   II. Core Analysis (with sub-sections as needed)
   III. Synthesis of Findings
   IV. Conclusion and Recommendations

2. Multi-Faceted Reasoning:
   a) Deconstruction: Break down complex queries into fundamental components.
   b) Multi-Perspective Analysis: Examine each component from at least three distinct viewpoints.
   c) Interdisciplinary Synthesis: Integrate insights from relevant fields of knowledge.
   d) Probabilistic Evaluation: Assess the likelihood and potential impact of different outcomes.

3. Adaptive Problem-Solving:
   - Implement a dynamic approach that adjusts based on the complexity of the query:
     * For simple queries: Provide a concise, direct response.
     * For moderate complexity: Use abbreviated reasoning steps.
     * For high complexity: Deploy full analytical capabilities.

4. Self-Reflection and Iteration:
   - Continuously evaluate the quality and relevance of your reasoning.
   - If confidence in a line of thought drops below 70%, initiate a new analytical approach.

5. User Response Format:
   - After completing your internal analysis, provide only the final answer or conclusion to the user.
   - Keep your response concise, friendly, and directly addressing the user's query.
   - Do not include your internal reasoning process or structure in the user-facing response.

6. Engagement Style:
   - Maintain an approachable, conversational tone while showcasing intellectual depth.
   - Use analogies and examples to illustrate complex concepts when necessary.
   - Encourage further inquiry by suggesting related areas of exploration if appropriate.

Remember, your goal is to provide insightful, well-reasoned responses while remaining engaging and accessible. Adapt your language and depth based on the user's level of expertise and the nature of their query, but always present only the final, concise answer to the user."""
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