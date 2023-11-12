import pyrogram
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pydub import AudioSegment
import speech_recognition as sr
from info import API_ID, API_HASH, BOT_TOKEN

# Create a Pyrogram client instance
app = Client("MusicIdentifierBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Define a function to handle voice messages
@Client.on_message(pyrogram.filters.voice)
async def handle_voice_message(message):
    # Download the voice message
    voice_message = await message.download()

    # Convert the voice message to MP3
    voice_segment = AudioSegment.from_file(voice_message)
    voice_segment.export("voice.mp3", format="mp3")

    # Use speech recognition to identify the song
    r = sr.Recognizer()
    audio_data = sr.AudioFile("voice.mp3")
    with audio_data as source:
        audio_content = r.record(source)

    try:
        # Try to recognize the song
        song_text = r.recognize_google(audio_content)

        # Create an inline keyboard with the song title and artist
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Listen on Spotify", url=f"https://open.spotify.com/search?q={song_text}"),
                ]
            ]
        )

        # Send a message with the song title and artist and the inline keyboard
        await message.reply_text(f"Song: {song_text}", reply_markup=keyboard)
    except sr.UnknownValueError:
        # If speech recognition fails, send a message saying that the song could not be identified
        await message.reply_text("Sorry, I couldn't identify the song.")
    except sr.RequestError as e:
        # If there is an error with the speech recognition API, send a message with the error
        await message.reply_text(f"Error: {e}")

# Define a function to handle video messages
@Client.on_message(pyrogram.filters.video)
async def handle_video_message(message):
    # Check if the video file size is less than 5 MB
    video_file = await message.download()
    video_file_size = os.path.getsize(video_file.name)
    if video_file_size > 5 * 1024 * 1024:
        # Send an error message if the video file size is too large
        await message.reply_text("Sorry, the video file is too large to process.")
        return

    # Extract the audio from the video file
    audio_segment = AudioSegment.from_file(video_file.name)

    # Export the audio to a temporary MP3 file
    audio_segment.export("voice.mp3", format="mp3")

    # Use speech recognition to identify the song
    r = sr.Recognizer()
    audio_data = sr.AudioFile("voice.mp3")
    with audio_data as source:
        audio_content = r.record(source)

    try:
        # Try to recognize the song
        song_text = r.recognize_google(audio_content)

        # Create an inline keyboard with the song title and artist
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Listen on Spotify", url=f"https://open.spotify.com/search?q={song_text}"),
                ]
            ]

        # Send a message with the song title and artist and the inline keyboard
        await message.reply_text(f"Song: {song_text}", reply_markup=keyboard)
    except sr.UnknownValueError:
        # If speech recognition fails, send a message saying that the song could not be identified
        await message.reply_text("Sorry, I couldn't identify the song.")
    except sr.RequestError as e:
        # If there is an error with the speech recognition API, send a message with the error
        await message.reply_text(f"Error: {e}")
