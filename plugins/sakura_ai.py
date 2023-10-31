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
from info import API_ID, API_HASH, BOT_TOKEN, GENERATIVE_AI_API_KEY
from google.generativeai import generate_text

client = Client(name="BardBot")

async def interact_with_bard(message):
  user_message = message_text

  # Send a message to the user if they have not provided a message
  if not user_message:
   await client.send_message(message.chat.id, "Please provide a message.")
   return

  response = await generate_response(user_message)

 # Send the response to the user
  await client.send_message(message.chat.id, response)

async def generate_response(prompt, timeout=10):
  headers = {
    "Authorization": "Bearer AIzaSyBlmXtVe1J2_6tyWtRFP0_iHSokXkGp3XQ"
  }
  response = await requests.post(
    "https://ai.google/generate",
    headers=headers,
    json={"prompt": prompt},
    timeout=timeout
  )
  response.raise_for_status()
  return response.json()["responses"][0]["text"]

@client.on_message(filters.command("sakura_ai"))
async def sakura_ai(client, message):
  await interact_with_bard(message)

