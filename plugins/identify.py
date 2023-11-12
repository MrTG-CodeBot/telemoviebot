import requests
from pyrogram import Client, filters
import acrcloud
from info import API_ID, API_HASH, BOT_TOKEN

# ACRCloud configuration for song recognition
config = {
    'host': 'identify-ap-southeast-1.acrcloud.com',
    'key': '0db9a34202c7797b535cba436dc24d07',
    'secret': 'XgSS5vWJ172QYhulX9WABchXNekBflz6mei5bJCy',
}

# Establishing a connection with ACRCloud service
acrcloud_client = acrcloud.ACRCloudRecognizer(config)

# Function to recognize songs from voice/audio messages
@Client.on_message(filters.voice | filters.audio)
async def recognize_song(client, message):
    # Download the received audio file
    audio_file = await message.download()
    
    # Use ACRCloud to recognize the song from the audio file
    result = acrcloud_client.recognize_by_file(audio_file, 0)
    
    # Extract song information if recognition is successful
    if 'metadata' in result and 'music' in result['metadata']:
        song_info = result['metadata']['music'][0]
        song_name = song_info['title']
        artist_name = song_info['artists'][0]['name']
        
        # Respond with recognized song and artist information
        await message.reply_text(f"Song: {song_name}\nArtist: {artist_name}")
    else:
        # Handle cases where no song is recognized
        await message.reply_text("Sorry, I couldn't recognize the song.")
