import os
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message
from info import API_ID, API_HASH, BOT_TOKEN, GOOGLE_BARD_API_KEY

GOOGLE_BARD_API_KEY = os.environ.get('AIzaSyBHHKi9eI9NSoPb_MMjsYSTGqE-bFPU2DE')

@Client.on_message(filters.command("ai"))
async def ai(client, message):
  # Get the user's message text.
  message_text = message.text

  # Send the request to the Bard API
  response = await client.send_message(
    message.chat.id,
    text="**Wait for the response from Sakura AI...**",
  )

  # Generate a response using Google Bard.
  bard_response = await bard_client.generate(
    prompt=message_text,
    max_tokens=1024,
    temperature=0.7
  )

  # Edit the original message with the response from Google Bard.
  await client.edit_message_text(
    message.chat.id,
    response.message_id,
    text=bard_response,
 )

 # Send the response to the user.
  await message.reply_text(response)
