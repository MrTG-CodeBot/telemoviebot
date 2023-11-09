import pyrogram
import requests
from pyrogram import Client, filters
from pysrt import SubRipFile
from info import API_ID, API_HASH, BOT_TOKEN

@client.on_message(filters.command("subtitle"))
async def subtitle(client, message):
        if message.text.startswith('/subtitle'):
            movie_name = message.text.split()[1]
            year = message.text.split()[2]

            try:

                subtitles_url = await self.get_subtitle_url(movie_name, year)

                subtitle_file = await self.download_subtitle(subtitles_url)

                await self.send_document(message.chat.id, subtitle_file)
            except Exception as e:

                print(e)
                await self.send_message(message.chat.id, f"Failed to download subtitles for {movie_name}: {e}")

    async def get_subtitle_url(self, movie_name, year):
       

        response = requests.get('https://api.opensubtitles.org/search/subtitles', params={
            'q': movie_name,
            'y': year
        })

        if response.status_code != 200:
            raise Exception('Failed to get subtitles URL')

        subtitles_list = response.json()['data']

        return subtitles_list[0]['zip_download_link']

    async def download_subtitle(self, subtitles_url):
        import requests

        response = requests.get(subtitles_url)

        with open('subtitles.srt', 'wb') as f:
            f.write(response.content)

        return 'subtitles.srt'

