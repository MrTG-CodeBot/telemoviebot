from pyrogram import Client, filters
import openai  # You'll need to install the 'openai' library
from info import OPENAI_API_KEY

# Create a dictionary to track user conversation context
user_context = {}

# Define a command to chat with the AI
@Client.on_message(filters.command("ai"))
def chat_with_ai(_, message):
    user_id = message.from_user.id
    user_message = message.text.split(" ", 1)[1]

    # Retrieve and update the user's conversation context
    context = user_context.get(user_id, "")
    context += f"User: {user_message}\n"

    # Use OpenAI's API to send the user's message and get a response
    response = openai.Completion.create(
        engine="davinci",
        prompt=context,
        max_tokens=50
    )

    ai_response = response.choices[0].text.strip()

    # Update the conversation context for the user
    context += f"AI: {ai_response}\n"
    user_context[user_id] = context

    # Send the AI's response to the user
    message.reply(f"AI: {ai_response}")
