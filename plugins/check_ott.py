from pyrogram import Client, filters
from info import API_ID,API_HASH,BOT_TOKEN


@Client.on_message(filters.command("/check_ott"))
async def search_movie(client, message):
    # Extract the user's query
    query = message.text.split(" ", 1)[1]

    # Use your chosen movie/series database or API to retrieve information
    # Replace this with your actual database/API request
    result = search_movie_in_database(query)

    if result:
        release_date = result.get("release_date", "Release date not found")
        ott_platform = result.get("ott_platform", "OTT platform not found")
        response = f"Release Date: {release_date}\nOTT Platform: {ott_platform}"
    else:
        response = "Movie/series not found."

    # Send the response to the user
    await message.reply(response)

