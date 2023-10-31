import asyncio
import json
import requests
import pyrogram
import bardapi
from bardapi import Bard
from pyrogram import Client, filters
from pyrogram.types import Message
from info import API_ID, API_HASH, BOT_TOKEN, BARD_API_TOKEN

bard_api_token = BARD_API_TOKEN

Client('bot', API_ID, API_HASH, BOT_TOKEN)
bard = Bard(bard_api_token)

# Add a command handler for the `/bard` command.
@Client.on_message(filters.command(["bard"]) & filters.text)
async def bard_ai(client: Client, message: Message):
    bard_response = bard.get_service_status()
    if bard_response['status'] != 'success':
        await message.reply_text('The Bard AI service is currently unavailable.')
        return

    prompt = message.text[len('/bard'):].strip()

    response = bard.get_answer(prompt)

    if response['status'] == 'success':
        # Success!
        generated_text = response['answer']

        await message.edit_text(generated_text)

    else:
        # Error!
        await message.reply_text('An error occurred while processing your request.')

# Handle all messages, regardless of whether they start with `/bard`.
@Client.on_message()
async def handle_message(client: Client, message: Message):
    if message.text.startswith('/bard'):
        await bard_ai(client, message)

