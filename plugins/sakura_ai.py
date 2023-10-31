import re
import os
from os import environ
from pyrogram import enums
import asyncio
import json
from pyrogram import Client, filters

# Replace these values with your own Telegram bot token and Google Bard AI API key
API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GOOGLE_BARD_AI_API_KEY = os.environ.get("GOOGLE_BARD_AI_API_KEY")

# A function to generate text using Google Bard AI
def generate_text(prompt):
  import requests

  headers = {
    "Authorization": f"Bearer {GOOGLE_BARD_AI_API_KEY}",
  }

  body = {
    "prompt": prompt,
  }

  response = requests.post(
    "https://ai.google/bard/api/generate",
    headers=headers,
    json=body,
  )

  try:
    response.raise_for_status()
  except requests.exceptions.HTTPError as e:
    print(e)
    return None

  return response.json()["text"]

client = Client("my_bot", api_token=API_TOKEN)

# Help command handler
@client.on_message(filters.command("help"))
def help_command(client, message):
  # Send a help message to the user
  client.send_message(message.chat.id, "Commands:\n/bard <prompt>: Generate text using Google Bard AI.\n/help: Show this help message.")

# Command handler for the `/bard` command
@client.on_message(filters.command("bard"))
def bard_command(client, message):
  # Generate text using Google Bard AI and send it to the user
  text = generate_text(message.text.split()[1])
  client.send_message(message.chat.id, text)


