import requests
from pyrogram import Client, filters
import acrcloud
import logging
from info import API_ID, API_HASH, BOT_TOKEN

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = {
    'host':'identify-ap-southeast-1.acrcloud.com',
    'key':'0db9a34202c7797b535cba436dc24d07',
    'secret':'XgSS5vWJ172QYhulX9WABchXNekBflz6mei5bJCy',
}

acrcloud_client = acrcloud.ACRCloudRecognizer(config)

@Client.on_message(filters.voice | filters.audio)
async def song_recognizer(client, message):
    try:
        song = await message.download()
        result = acrcloud_client.recognize_by_file(song, 0)
        if 'metadata' in result and 'music' in result['metadata']:
            song_info = result['metadata']['music'][0]
            song_name = song_info['title']
            artist_name = song_info['artists'][0]['name']
            await message.reply_text(f"Song: {song_name}\nArtist: {artist_name}")
        else:
            logger.error(f"No music data in the recognition result: {result}")
            await message.reply_text("Sorry, I couldn't recognize the song.")
    except Exception as e:
        logger.error(f"An error occurred while recognizing the song: {e}")
        await message.reply_text("Sorry, an error occurred while recognizing the song.")
