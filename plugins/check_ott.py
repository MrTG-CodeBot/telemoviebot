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
            plot = data.get("Plot", "No plot available.")
            released = data.get("Released", "N/A")
            ratings = data.get("Ratings", [])
            ott_platform = data.get("Website", "N/A")

            ott_status = f"Title: {title}\nReleased: {released}\nPlot: {plot}"

            if ott_platform == "N/A":
                ott_status += "\nNot available on any OTT platform."
            else:
                ott_status += f"\nAvailable on {ott_platform}."

            if ratings:
                ott_status += f"\nRatings:"
                for rating in ratings:
                    source = rating.get("Source", "N/A")
                    value = rating.get("Value", "N/A")
                    ott_status += f"\n- {source}: {value}"

            await message.reply_text(ott_status)
        else:
            await message.reply_text("Movie not found. Please check the movie title.")
    else:
        await message.reply_text("An error occurred while fetching movie data. Please try again later.")

