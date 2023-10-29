import os
import openai
from pyrogram import Client, filters
from pyrogram.types import Message
from info import API_ID,API_HASH, BOT_TOKEN, OPENAI_API_KEY

# Set your OpenAI API key
openai.api_key = OPENAI_API_KEY

# Define a command for users to ask questions
@Client.on_message(filters.command("ask", prefixes="/"))
def ask_question_command(client: Client, message: Message):
    # Extract the user's question from the command
    user_question = message.text.split(" ", 1)[1]

    # Define a system message and user message
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_question}
    ]

    # Call the OpenAI API to get a response
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use "gpt-4" if you have early access, otherwise "gpt-3.5-turbo"
        messages=messages
    )

    # Send the AI response to the user
    assistant_response = response['choices'][0]['message']['content']
    message.reply(assistant_response)
