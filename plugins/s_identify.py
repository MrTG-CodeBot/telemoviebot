import acrcloud
from info import API_ID, API_HASH, BOT_TOKEN

from pyrogram import Client, filters
import requests
import json

# Supported audio formats
supported_audio_formats = ['mp3', 'wav', 'flac', 'ogg']

# Function to recognize music
def recognize_music(audio_file):
    # Use the music recognition API (e.g., ACRCloud)
    # Send audio data to the API and get the recognition result
    # Replace 'YOUR_ACR_API_KEY' and 'YOUR_ACR_API_SECRET' with actual ACRCloud credentials
    url = "http://identify.acrcloud.com/v1/identify"
    headers = {
        'host':'identify-ap-southeast-1.acrcloud.com',
        'access_key': '0db9a34202c7797b535cba436dc24d07',
        'access_secret': 'XgSS5vWJ172QYhulX9WABchXNekBflz6mei5bJCy',
        'Content-Type': 'application/octet-stream'
    }

# Command to recognize music
@Client.on_message(filters.command("recognize"))
def recognize_command(client, message):
    # Check if the message contains an audio file
    if message.audio:
        audio_file = message.download()
        audio_extension = audio_file.split('.')[-1]

        # Check if the audio format is supported
        if audio_extension.lower() not in supported_audio_formats:
            client.send_message(message.chat.id, f"Unsupported audio format: {audio_extension}. Supported formats: {', '.join(supported_audio_formats)}")
            return

        result = recognize_music(audio_file)

        # Send the recognition result back to the user
        if result:
            client.send_message(message.chat.id, f"Music recognized:\n\nTitle: {result['title']}\nArtist: {result['artist']}\nAlbum: {result['album']}\nGenre: {result['genre']}\nRelease Date: {result['release_date']}")
        else:
            client.send_message(message.chat.id, "Failed to recognize music. Please try again.")
    else:
        client.send_message(message.chat.id, "Please send an audio file for recognition.")
    
    # Make a POST request with the audio file
    with open(filename, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, headers=headers, files=files)

    # Process the response and extract recognized music information
    # You'll need to handle the response based on the ACRCloud API documentation
    try:
        response_json = json.loads(response.text)
        music_info = response_json['results'][0]['items'][0]
        music_title = music_info['title']
        music_artist = music_info['artists'][0]['name']
        music_album = music_info['album']['name']
        music_genre = music_info['genres'][0]['name']
        music_release_date = music_info['release_date']

        return {
            'title': music_title,
            'artist': music_artist,
            'album': music_album,
            'genre': music_genre,
            'release_date': music_release_date
        }
    except:
        return None