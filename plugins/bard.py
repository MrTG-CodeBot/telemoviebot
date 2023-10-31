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

client = Client('bot', API_ID, API_HASH, BOT_TOKEN)
bard = Bard(bard_api_token)

# Add a command handler for the `/bard` command.
@client.on_message(filters.command(["bard"]) & filters.text)
async def bard_ai(client: Client, message: Message):
    # Check if the Bard AI service is available.
    bard_response = bard.get_service_status()
    if bard_response['status'] != 'success':
        await message.reply_text('The Bard AI service is currently unavailable.')
        return

    # Get the prompt from the message.
    prompt = message.text[len('/bard'):].strip()

    # Check if the __Secure-1PSID cookie ends with a single dot.
    cookie_value = requests.utils.get_cookie_header(['__Secure-1PSID'])
    if not check_secure_1psid(cookie_value):
        # Raise an error if the value of the cookie does not end with a single dot.
        await message.reply_text('__Secure-1PSID value must end with a single dot. Enter correct __Secure-1PSID value.')
        return

    # Set the __Secure-1PSID cookie on the Bard object.
    bard.session.cookies.set('__Secure-1PSID', cookie_value)

    # Get the answer to the prompt.
    response = bard.get_answer(prompt)

    # If the response is successful, send the answer to the user.
    if response['status'] == 'success':
        await message.edit_text(response['answer'])

    # Otherwise, send an error message to the user.
    else:
        await message.reply_text('An error occurred while processing your request.')

# Handle all messages, regardless of whether they start with `/bard`.
@client.on_message()
async def handle_message(client: Client, message: Message):
    if message.text.startswith('/bard'):
        await bard_ai(client, message)
