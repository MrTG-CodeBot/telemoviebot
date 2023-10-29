import os
import openai
from pyrogram import Client, filters
from pyrogram.types import Message
from info import API_ID, API_HASH, BOT_TOKEN, OPENAI_API_KEY, OPENAI_ORGANIZATION

OPENAI_API_KEY = os.environ.get("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")
OPENAI_ORGANIZATION = os.environ.get('org-63EsIa4XvrrUsETGhjsDzYIq')

@Client.on_message(filters.command("ask"))
async def gpt_command(client, message):
    try:
        input_text = " ".join(message.text.split()[1:])
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=input_text,
            max_tokens=50  # Adjust this as needed
        )
        response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)
        await message.reply(response.choices[0].text)
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
# Define a command to check the request count
@Client.on_message(filters.command("request_count", prefixes="/"))
def check_request_count(client: Client, message: Message):
    global request_count  # Access the request_count variable
    message.reply(f"Number of requests: {request_count}")
