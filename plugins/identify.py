import os
import uuid
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pydub import AudioSegment
import speech_recognition as sr
from info import API_ID, API_HASH, BOT_TOKEN


@Client.on_message(filters.voice)
async def handle_voice_message(client, message):
    voice_message = await message.download()
    voice_segment = AudioSegment.from_file(voice_message)
    voice_file_path = f"{uuid.uuid4()}.mp3"
    voice_segment.export(voice_file_path, format="mp3")
    song_text = transcribe_audio(voice_file_path)
    if song_text:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Listen on Spotify", url=f"https://open.spotify.com/search?q={song_text}")]])
        await message.reply_text(f"Song: {song_text}", reply_markup=keyboard)
    else:
        await message.reply_text("Sorry, I couldn't identify the song.")
    os.remove(voice_file_path)

@Client.on_message(filters.video)
async def handle_video_message(client, message):
    if message.video.file_size > 5 * 1024 * 1024:
        await message.reply_text("Sorry, the video file is too large to process.")
        return
    video_file = await message.download()
    audio_segment = AudioSegment.from_file(video_file)
    voice_file_path = f"{uuid.uuid4()}.mp3"
    audio_segment.export(voice_file_path, format="mp3")
    song_text = transcribe_audio(voice_file_path)
    if song_text:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Listen on Spotify", url=f"https://open.spotify.com/search?q={song_text}")]])
        await message.reply_text(f"Song: {song_text}", reply_markup=keyboard)
    else:
        await message.reply_text("Sorry, I couldn't identify the song.")
    os.remove(voice_file_path)

