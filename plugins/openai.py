import os
from pyrogram import Client, filters
import openai
from plugins import openai_work
from info import API_ID, API_HASH, BOT_TOKEN, OPEN_API_KEY, OPENAI_ORGANIZATION

openai.api_key = OPEN_API_KEY
openai.organization = OPENAI_ORGANIZATION

@Client.on_message(filters.command("openai"))
async def openai(client, message):
    prompt = message.text.split(" ", 1)[1]  # Get the text after the /openai command

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=100,
    )

    await client.send_message(chat_id=message.chat.id, text=response.choices[0].text.strip())
