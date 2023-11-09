import os
import requests
from pyrogram import Client, filters

@Client.on_message(filters.command("generate"))
async def generate(client, message):
    try:
        response = requests.get('https://thisanimedoesnotexist.ai')
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        await message.reply_text(f"Failed to generate an image. Error: {err}")
        return

    file_name = f"anime_character.jpg"
    try:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        with open(file_name, 'rb') as img:
            await client.send_photo(chat_id=message.chat.id, photo=img)
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
