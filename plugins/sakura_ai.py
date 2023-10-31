import re
import os
from os import environ
from pyrogram import enums
import asyncio
import json
from pyrogram import Client, filters

import pyrogram
from pyrogram import Client
import requests
from info import API_ID, API_HASH, BOT_TOKEN

client = Client(
    name="BardBot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

def interact_with_bard(prompt):
    headers = {
        "Authorization": "Bearer YOUR_GENERATIVE_AI_API_KEY"
    }
    response = requests.post(
        "https://ai.google/generate",
        headers=headers,
        json={"prompt": prompt}
    )
    response.raise_for_status()
    return response.json()["responses"][0]["text"]

@client.on_message(filters.command("sakura_ai"))
def sakura_ai(client, message):
    # Get the user's message
    user_message = message.text

    # Generate a response using the Generative AI API
    response = interact_with_bard(user_message)

    # Send the response to the user
    client.send_message(message.chat.id, response)
