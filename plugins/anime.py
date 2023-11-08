# LIVDSRZULELA
from pyrogram import Client, filters
import requests

@filters.command("anime_quote")
async def on_message(self, message):
        try:
            quote = self.get_anime_quote()
            await message.reply_text(quote)
        except Exception as e:
            logging.error(f"An error occurred: {e}")

@filters.command("anime_gif")
async def on_gif_message(self, message):
        try:
            gif_url = self.get_anime_gif()
            await message.reply_animation(gif_url)
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def get_anime_quote(self):
        try:
            response = requests.get('https://animechan.vercel.app/api/random')
            response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
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

