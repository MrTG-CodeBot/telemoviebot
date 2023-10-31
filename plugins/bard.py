import asyncio
import json
import requests
import pyrogram
import bardapi
from bardapi import Bard
from info import API_ID, API_HASH, BOT_TOKEN, BARD_API_TOKEN 
from pyrogram import Client, filters
from pyrogram.types import Message

bard_api_token = 'BARD_API_TOKEN'

Client('bot', api_id, api_hash, bot_token)
bard = bardapi.core.Bard(bard_api_token)

# Add a command handler for the `/bard` command.
@Client.on_message(filters.command(["bard"]))
async def bard_ai(client: Client, message: Message):
  """Handles Bard AI requests."""

  # Get the prompt from the message.
  prompt = message.text[len('/bard'):].strip()

  # Make a request to the Bard AI API.
  response = bard.get_answer(prompt)

  # Check the response status code.
  if response['status'] == 'success':
    # Success!
    generated_text = response['answer']

    # Send the generated text back to the user.
    await message.reply_text(generated_text)

  else:
    # Error!
    await message.reply_text('An error occurred while processing your request.')

# Handle all other messages.
@Client.on_message()
async def handle_message(client: Client, message: Message):
  """Handles all incoming messages."""

  # Ignore the message if it's not a Bard AI request.
  if not message.text.startswith('/bard'):
    return

  # Otherwise, handle the Bard AI request.
  await bard_ai(client, message)
