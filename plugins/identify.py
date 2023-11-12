from pyrogram import Client, filters
import acrcloud
import requests

config = {
    'host':'host',
    'key':'api_key',
    'secret':'api_secret',
}

acrcloud_client = acrcloud.ACRCloudRecognizer(config)

app = Client("my_bot", bot_token="your_bot_token")

@app.on_message(filters.voice | filters.audio)
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
    headers = {"Authorization": "Bearer your_token"}  # Replace with your actual token
    params = {"q": search_query, "type": "track"}
    response = requests.get(download_url, headers=headers, params=params)
    download_link = response.json()['tracks']['items'][0]['preview_url']
    song_data = requests.get(download_link).content
    with open(f"{song_name}.mp3", "wb") as f:
        f.write(song_data)
    await message.reply_audio(audio=f"{song_name}.mp3")


