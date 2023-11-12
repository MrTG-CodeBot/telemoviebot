import asyncio
import logging
from pyrogram import Client, filters
from info import API_ID, API_HASH, BOT_TOKEN
import acrcloud
import ffmpeg

config = {
    'host': 'host',
    'key': 'api_key',
    'secret': 'api_secret',
}

acrcloud_client = acrcloud.ACRCloudRecognizer(config)

def convert_to_mp3(audio_file):
    logging.info(f"Converting audio file to MP3: {audio_file}")
    try:
        ffmpeg.input(audio_file).output(audio_file.replace('.wav', '.mp3')).run()
    except Exception as e:
        logging.error(f"Failed to convert audio file: {e}")
        return None

def recognize_song(audio_file):
    logging.info(f"Recognizing song from WAV file: audio.wav")
    try:
        result = acrcloud_client.recognize_by_file('audio.wav', 0)
        return result
    except Exception as e:
        logging.error(f"Failed to recognize song: {e}")
        return None

def estimate_song_duration(audio_file):
    logging.info(f"Estimating song duration: {audio_file}")
    try:
        probe = ffmpeg.probe(audio_file)
        duration = probe['format']['duration']
        return duration
    except Exception as e:
        logging.error(f"Failed to estimate song duration: {e}")
        return None

async def song_recognizer(client, message):
    # Download the audio file
    logging.info(f"Downloading audio file: {message.id}")
    audio_file = await message.download()

    # Convert the audio file to WAV format if necessary
    if audio_file.endswith('.mp3') or audio_file.endswith('.ogg'):
        logging.info(f"Converting audio file to WAV: {audio_file}")
        converted_audio_file = await asyncio.to_thread(convert_to_wav, audio_file)
        if converted_audio_file is None:
            return

        audio_file = converted_audio_file

    # Estimate the song duration
    duration = await asyncio.to_thread(estimate_song_duration, audio_file)

    # Recognize the song using ACRCloud
    result = await asyncio.to_thread(recognize_song, audio_file)

    # Reply with the song recognition result
    if result:
        await message.reply_text(result)

    # Convert the recognized song to MP3
    if result:
        logging.info(f"Converting recognized song to MP3: audio.wav")
        try:
            ffmpeg.input(audio_file).output(f"{result['id']}.mp3").run()
        except Exception as e:
            logging.error(f"Failed to convert recognized song: {e}")

    # Delete the temporary WAV file
    if audio_file.endswith('.wav'):
        logging.info(f"Deleting temporary WAV file: audio.wav")
        try:
            os.remove('audio.wav')
        except Exception:
            pass

    # Inform user about song duration if available
    if duration:
        await message.reply_text(f"Song duration: {duration} seconds")
