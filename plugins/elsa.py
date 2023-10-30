import os
import pyrogram
import bard
from pyrogram import Client, filters
from pyrogram.types import Message
from info import API_ID, API_HASH, BOT_TOKEN, GOOGLE_BARD_API_KEY

GOOGLE_BARD_API_KEY = os.environ.get('AIzaSyBHHKi9eI9NSoPb_MMjsYSTGqE-bFPU2DE')

# Define the bard_client variable.
bard_client = bard.Client(api_key=GOOGLE_BARD_API_KEY)

@Client.on_message(filters.command("ai"))
async def ai(client, message):

    # Get the user's message text.
    message_text = message.text

    # Generate a response using Google Bard.
    bard_response = await bard_client.generate(
        prompt=message_text,
        max_tokens=1024,
        temperature=0.7
    )

    # Send the response to the user.
    await message.reply_text(bard_response)
