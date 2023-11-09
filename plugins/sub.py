import pyrogram
import requests
from pyrogram import Client, filters
from pysrt import SubRipFile
from info import API_ID, API_HASH, BOT_TOKEN

@Client.on_message(filters.command("subtitle"))
async def subtitle(client, message):
    movie_name, year = message.text.split()[1:]
    subtitles_url = await get_subtitle_url(movie_name, year)
    subtitle_file = await download_subtitle(subtitles_url)
    await client.send_document(chat_id=message.chat.id, document=open(subtitle_file, 'rb'))

async def get_subtitle_url(movie_name, year):
    response = requests.get('https://api.opensubtitles.org/search/subtitles', params={
        'q': movie_name,
        'y': year
    })

    if response.status_code != 200:
        raise Exception('Failed to get subtitles URL')

    subtitles_list = response.json()['data']
    return subtitles_list[0]['zip_download_link']

async def download_subtitle(subtitles_url):
    try:
        response = requests.get(subtitles_url)

        with open('subtitles.srt', 'wb') as f:
            f.write(response.content)
    finally:
        if f:
            f.close()

    return 'subtitles.srt'
