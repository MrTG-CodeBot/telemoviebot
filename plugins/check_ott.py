import asyncio
from pyrogram import Client, filters
import requests
from info import OMDB_API_KEY

# Define a command to check OTT release
@Client.on_message(filters.command("checkott"))
async def check_ott_release(_, message):
    # Get the movie title from the user's command
    if len(message.command) < 2:
        await message.reply_text("Please provide the movie title with the command.")
        return

    movie_title = " ".join(message.command[1:])

    # Send a request to the OMDb API to retrieve movie information
    omdb_url = f"http://www.omdbapi.com/?t={movie_title}&apikey=42d8ac83"
    response = requests.get(omdb_url)

    if response.status_code == 200:
        data = response.json()
        if data.get("Response", "").lower() == "true":
            title = data.get("Title", "N/A")
            ott_platform = data.get("Website", "N/A")
            if ott_platform == "N/A":
                ott_status = "Not available on any OTT platform."
            else:
                ott_status = f"Available on {ott_platform}."

            ott_release_message = f"{title}:\n{ott_status}"
            await message.reply_text(ott_release_message)
        else:
            await message.reply_text("Movie not found. Please check the movie title.")
    else:
        await message.reply_text("An error occurred while fetching movie data. Please try again later.")
