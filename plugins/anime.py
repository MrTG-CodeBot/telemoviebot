from pyrogram import Client, filters
import requests
import logging

class AnimeBot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@Client.on_message(filters.command("anime_quote") & filters.private & filters.incoming)
 async def on_message(self, message):
        try:
            quote = self.get_anime_quote()
            await message.reply_text(quote)
        except Exception as e:
            logging.error(f"An error occurred: {e}")

@Client.on_message(filters.command("anime_gif") & filters.private & filters.incoming)
    async def on_gif_message(self, message):
        try:
            gif_url = self.get_anime_gif()
            await message.reply_animation(gif_url)
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def get_anime_quote(self):
        try:
            response = requests.get('https://animechan.vercel.app/api/random')
            response.raise_for_status() 
            json = response.json()
            quote = json["quote"]
            anime = json["anime"]
            character = json["character"]
            return f'"{quote}" - {character} ({anime})'
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return "Sorry, I couldn't fetch an anime quote at the moment."

    def get_anime_gif(self):
        try:
            response = requests.get('https://api.tenor.com/v1/random?q=anime&key=LIVDSRZULELA&limit=1')
            response.raise_for_status()
            json = response.json()
            gif_url = json['results'][0]['media'][0]['gif']['url']
            return gif_url
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return "Sorry, I couldn't fetch an anime gif at the moment."
