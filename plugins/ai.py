import pyrogram
import bardapi
import request
from pyrogram import Client, filters
from pyrogram.types import Message
from info import API_ID, API_HASH, BOT_TOKEN, GOOGLE_BARD_API_KEY

bard_client = bard.Client(api_key="AIzaSyBHHKi9eI9NSoPb_MMjsYSTGqE-bFPU2DE")


@Client.on_message(filters.command("ai"))
async def ai(client, message):
    # Get the user's message text.
    message_text = message.text

    # Send the request to the Bard API
    response = await client.send_request(
        "https://language.googleapis.com/v1beta1/generation/",
        method="POST",
        data={"input_text": request},
    )


    # Generate a response using Google Bard.
    response = await bard_client.generate(
        prompt=message_text,
        max_tokens=1024,
        temperature=0.7
    )

    # Send the response to the user.
    await message.reply_text(response)
