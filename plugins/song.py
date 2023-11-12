import pyrogram
from pyrogram import Client, Filters, InlineKeyboardMarkup, InlineKeyboardButton
from pydub import AudioSegment
from spotipy import Spotify
from fuzzywuzzy import fuzz
from youtube_dl import YoutubeDL
import requests
import json
import os
import ffmpeg

# Initialize Spotify API
sp = Spotify(auth_manager=SpotifyOAuth(client_id="YOUR_SPOTIFY_CLIENT_ID",
                                      client_secret="YOUR_SPOTIFY_CLIENT_SECRET",
                                      redirect_uri="YOUR_SPOTIFY_REDIRECT_URI"))

# Initialize YouTube downloader
ydl_opts = {"format": "bestaudio/bestvideo[ext=mp4]+bestaudio/best[ext=m4a]/mp3"}
ydl = YoutubeDL(ydl_opts)

# Song recognition function
def recognize_song(audio_file):
    # Extract audio fingerprint using pydub
    try:
        segment = AudioSegment.from_file(audio_file)
        fingerprint = segment.fingerprint()
    except ValueError:
        return "Invalid audio file"

    # Search for matching songs on Spotify
    results = []
    for song in sp.search(query=fingerprint, type="track")["tracks"]["items"]:
        track_name = song["name"]
        artist_name = song["artists"][0]["name"]
        score = fuzz.ratio(fingerprint, song["audio_features"]["mfid"])
        results.append((score, track_name, artist_name))

    # Sort results by similarity score
    results.sort(key=lambda x: x[0], reverse=True)

    # Return the top result
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
def search_song(query):
    # Search for songs on Spotify
    try:
        results = sp.search(query=query, type="track")["tracks"]["items"]
    except:
        return "Error searching for songs"

    # Create inline keyboard buttons for each result
    buttons = []
    for song in results:
        track_name = song["name"]
        artist_name = song["artists"][0]["name"]
        track_id = song["id"]

        button = InlineKeyboardButton(f"{track_name} by {artist_name}", callback_data=f"download_{track_id}")
        buttons.append(button)

    # Create inline keyboard markup
    keyboard = InlineKeyboardMarkup(rows=[buttons])

    # Send message with inline keyboard
    app.send_message(chat_id, "Select the song you want to download:", reply_markup=keyboard)

# Download song from YouTube or Spotify
def download_song(message, callback_data):
    # Parse callback data
    action, track_id = callback_data.split("_")

    # Download song from YouTube
    if action == "download_youtube":
        # Get video URL from callback data
        video_url = message.reply_markup.inline_keyboardbuttons[0].url

        # Download video using youtube-dl
        try:
            with ydl.extract_info(video_url, download=False) as video_info:
                audio_url = video_info["formats"][-1]["url"]

            # Download audio file
            ydl.download([audio_url])

            # Send audio file to chat
            Client.send_audio(chat_id, f"music/{track_id}.mp3")
        except:
            Client.send_message(chat_id, "Error downloading song from YouTube")

    # Download song from Spotify
    if action == "download_spotify":
        # Get song details from Spotify API
        try:
                        song_info = sp.track(track_id)
            track_name = song_info["name"]
            artist_name = song_info["artists"][0]["name"]
            audio_url = song_info["preview_url"]

            # Download audio file from preview URL
            if audio_url is not None:
                response = requests.get(audio_url, stream=True)
                if response.status_code == 200:
                    with open(f"music/{track_id}.mp3", "wb") as audio_file:
                        audio_file.write(response.content)

                    # Convert audio file to desired format using ffmpeg
                    os.system(f"ffmpeg -i music/{track_id}.mp3 -acodec pcm_s16le -ac 2 -ar 44100 music/{track_id}.wav")

                    # Send audio file to chat
                   Client.send_audio(chat_id, f"music/{track_id}.wav")
                else:
                    Client.send_message(chat_id, "Sorry, the song preview is not available.")
            else:
                Client.send_message(chat_id, "Sorry, the song preview is not available.")
        except:
            Client.send_message(chat_id, "Error downloading song from Spotify")


