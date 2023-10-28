from pyrogram import Client, filters
from PIL import Image
from info import API_ID, API_HASH, BOT_TOKEN

# Define the required picture for the thumbnail
required_picture = Image.open("https://telegra.ph/file/fc67cc1d31af65967e4f9.jpg")

@Client.on_message(filters.document)
async def generate_thumbnail(client, message):
    # Get the document (file) sent by the user
    document = message.document

    # Download the document
    file_path = await client.download_media(document)

    # Generate the thumbnail by resizing the required picture
    thumbnail = required_picture.resize((100, 100))

    # Save the generated thumbnail as a file
    thumbnail_path = "thumbnail.jpg"
    thumbnail.save(thumbnail_path)

    # Send the generated thumbnail as a reply to the user
    await message.reply_photo(photo=thumbnail_path)

