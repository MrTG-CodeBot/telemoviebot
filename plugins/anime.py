import os
import requests
from pyrogram import Client, filters

@Client.on_message(filters.command("generate"))
async def generate(client, message):
    response = requests.get('https://thisanimedoesnotexist.ai/results?seed=0.1234567890123456')
    if response.status_code != 200:
        await message.reply_text("Failed to generate an image. Please try again later.")
        return

    file_name = f"anime_character_{message.message_id}.jpg"
    try:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        await client.send_photo(chat_id=message.chat.id, photo=open(file_name, 'rb'))
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
