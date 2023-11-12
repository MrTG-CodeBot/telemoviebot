import requests
from pyrogram import Client, filters
import acrcloud
from info import API_ID, API_HASH, BOT_TOKEN

def get_spotify_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': 21cf39f58bf7494d8fa377c59b72211c,
        'client_secret': cc98f5a4038e40a9adc7573bf5b072a5,
    })

    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    return access_token

config = {
    'host':'identify-ap-southeast-1.acrcloud.com',
    'key':'0db9a34202c7797b535cba436dc24d07',
    'secret':'XgSS5vWJ172QYhulX9WABchXNekBflz6mei5bJCy',
}

acrcloud_client = acrcloud.ACRCloudRecognizer(config)

@Client.on_message(filters.voice | filters.audio)
async def song_recognizer(client, message):
    song = await message.download()
    result = acrcloud_client.recognize_by_file(song, 0)
    song_info = result['metadata']['music'][0]
    song_name = song_info['title']
    artist_name = song_info['artists'][0]['name']
    await message.reply_text(f"Song: {song_name}\nArtist: {artist_name}")

    # Download the song
    search_query = f"{song_name} {artist_name}"
    download_url = "https://api.spotify.com/v1/search"  # Replace with the actual API
    headers = {"Authorization": f"Bearer {get_spotify_token('21cf39f58bf7494d8fa377c59b72211c', 'cc98f5a4038e40a9adc7573bf5b072a5t')}"}  # Replace with your actual token
    params = {"q": search_query, "type": "track"}
    response = requests.get(download_url, headers=headers, params=params)
    download_link = response.json()['tracks']['items'][0]['preview_url']
    song_data = requests.get(download_link).content
    with open(f"{song_name}.mp3", "wb") as f:
        f.write(song_data)
    await message.reply_audio(audio=f"{song_name}.mp3")
