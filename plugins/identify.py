import pyrogram
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pydub import AudioSegment
import speech_recognition as sr

@bot.on_message(pyrogram.filters.voice)
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

bot.run()
