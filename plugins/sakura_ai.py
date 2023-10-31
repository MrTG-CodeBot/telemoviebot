import re
import os
import asyncio
import json
from pyrogram import Client, filters
import requests
from info import API_ID, API_HASH, BOT_TOKEN, GENERATIVE_AI_API_KEY  # Assuming info.py contains these constants

client = Client("BardBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@client.on_message(filters.command("sakura_ai"))
async def sakura_ai_command_handler(client, message):
    user_message = message.text.split(maxsplit=1)
    if len(user_message) > 1:
        user_message = user_message[1]
        await interact_with_bard(message, user_message)
    else:
        await message.reply("Please provide a message.")

async def interact_with_bard(message, user_message):
    # Send a message to the user if they have not provided a message
    if not user_message:
        await message.reply("Please provide a message.")
        return

    response = await generate_response(user_message)

    # Send the response to the user
    await message.reply(response)

async def generate_response(prompt, timeout=10):
    headers = {
        "Authorization": AIzaSyBlmXtVe1J2_6tyWtRFP0_iHSokXkGp3XQ  # Use your actual API key
    }
    response = await requests.post(
        "https://ai.google/generate",  # Replace with the correct URL
        headers=headers,
        json={"prompt": prompt},
        timeout=timeout
    )
    response.raise_for_status()
    data = response.json()
    return data["responses"][0]["text"]
