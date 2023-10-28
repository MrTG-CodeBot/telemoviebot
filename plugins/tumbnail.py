from pyrogram import Client, filters
from PIL import Image
import requests
from io import BytesIO

# URL of the required picture for the thumbnail
required_picture_url = "https://telegra.ph/file/fc67cc1d31af65967e4f9.jpg"

@Client.on_message(filters.document)
async def generate_thumbnail(client, message):
    # Get the document (file) sent by the user
    document = message.document

    # Download the document
    file_path = await client.download_media(document)

    # Download the required picture from the URL
    response = requests.get(required_picture_url)
    required_picture = Image.open(BytesIO(response.content))

    # Generate the thumbnail by resizing the required picture
    thumbnail = required_picture.resize((100, 100))

    # Save the generated thumbnail as a file
    thumbnail_path = "thumbnail.jpg"
    thumbnail.save(thumbnail_path)

    # Send the generated thumbnail as a reply to the user
    await message.reply_photo(photo=thumbnail_path)

