# Copyright (c) 1987, 1993, 1994 The Regents of the University of
California.  All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1.  Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
2.  Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
3.  Neither the name of the University nor the names of its contributors
    may be used to endorse or promote products derived from this
    software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS “AS IS” AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.


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
