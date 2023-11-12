import pyrogram
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pydub import AudioSegment
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth  
from fuzzywuzzy import fuzz
from youtube_dl import YoutubeDL
import requests
import json
import os
import ffmpeg
from info import API_ID, API_HASH, BOT_TOKEN

# Initialize Spotify API
sp = Spotify(auth_manager=SpotifyOAuth(client_id="d211d50a2fd04b1fab37f49138efe3c6",
                                      client_secret="82cb098c25684ded949137884b5c0b17",
                                      redirect_uri="https://sakura.com/callback"))

# Initialize YouTube downloader
ydl_opts = {"format": "bestaudio/bestvideo[ext=mp4]+bestaudio/best[ext=m4a]/mp3"}
ydl = YoutubeDL(ydl_opts)

# Song recognition function
def recognize_song(audio_file):
    try:
        segment = AudioSegment.from_file(audio_file)
        fingerprint = segment.fingerprint()
    except ValueError:
        return "Invalid audio file"

    results = []
    for song in sp.search(q=fingerprint, type="track")["tracks"]["items"]:  # Changed 'query' to 'q'
        track_name = song["name"]
        artist_name = song["artists"][0]["name"]
        score = fuzz.ratio(fingerprint, song["audio_features"]["mfid"])
        results.append((score, track_name, artist_name))

    results.sort(key=lambda x: x[0], reverse=True)

    if results:
        best_match = results[0]
        score = best_match[0]
        track_name = best_match[1]
        artist_name = best_match[2]

        if score >= 90:
            return f"Song recognized: {track_name} by {artist_name} (Similarity: {score}%)"
        elif score >= 80:
            return f"Possible match: {track_name} by {artist_name} (Similarity: {score}%)"
        else:
            return "Song not recognized"
    else:
        return "Song not recognized"

# Song search function
def search_song(query, chat_id):  # Added chat_id parameter
    try:
        results = sp.search(query=query, type="track")["tracks"]["items"]
    except:
        return "Error searching for songs"

    buttons = []
    for song in results:
        track_name = song["name"]
        artist_name = song["artists"][0]["name"]
        track_id = song["id"]

        button = InlineKeyboardButton(f"{track_name} by {artist_name}", callback_data=f"download_{track_id}")
        buttons.append(button)

    keyboard = InlineKeyboardMarkup(rows=[buttons])

    Client.send_message(chat_id, "Select the song you want to download:", reply_markup=keyboard)

# Download song from YouTube or Spotify
def download_song(message, callback_data, chat_id):  # Added chat_id parameter
    action, track_id = callback_data.split("_")

    if action == "download_youtube":
        video_url = message.reply_markup.inline_keyboard[0][0].url  # Fixed attribute typo
        try:
            with ydl.extract_info(video_url, download=False) as video_info:
                audio_url = video_info["formats"][-1]["url"]

            ydl.download([audio_url])

            Client.send_audio(chat_id, f"music/{track_id}.mp3")
        except:
            Client.send_message(chat_id, "Error downloading song from YouTube")

    if action == "download_spotify":
        try:
            song_info = sp.track(track_id)
            track_name = song_info["name"]
            artist_name = song_info["artists"][0]["name"]
            audio_url = song_info["preview_url"]

            if audio_url is not None:
                response = requests.get(audio_url, stream=True)
                if response.status_code == 200:
                    with open(f"music/{track_id}.mp3", "wb") as audio_file:
                        audio_file.write(response.content)

                    os.system(f"ffmpeg -i music/{track_id}.mp3 -acodec pcm_s16le -ac 2 -ar 44100 music/{track_id}.wav")

                    Client.send_audio(chat_id, f"music/{track_id}.wav")
                else:
                    Client.send_message(chat_id, "Sorry, the song preview is not available.")
            else:
                Client.send_message(chat_id, "Sorry, the song preview is not available.")
        except:
            Client.send_message(chat_id, "Error downloading song from Spotify")
