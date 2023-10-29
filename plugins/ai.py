import os
import openai
from pyrogram import Client, filters
from pyrogram.types import Message
from info import API_ID, API_HASH, BOT_TOKEN, OPENAI_API_KEY, OPENAI_ORGANIZATION

# Initialize a variable to keep track of the number of requests
request_count = 0

# Set your OpenAI API key

openai.api_key = OPENAI_API_KEY
OpenAI-Organization = OPENAI_ORGANIZATION

# Define a command for users to ask questions
@Client.on_message(filters.command("ask", prefixes="/"))
def ask_question_command(client: Client, message: Message):
    global request_count  # Access the request_count variable

    try:
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

        # Increment the request count
        request_count += 1

    except Exception as e:
        # Handle any errors that occur during processing
        error_message = f"An error occurred: {str(e)}"
        message.reply(error_message)

# Define a command to check the request count
@Client.on_message(filters.command("request_count", prefixes="/"))
def check_request_count(client: Client, message: Message):
    global request_count  # Access the request_count variable
    message.reply(f"Number of requests: {request_count}")
