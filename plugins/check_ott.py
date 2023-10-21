from pyrogram import Client, filters
from imdb import IMDb
from info import API_ID,API_HASH,BOT_TOKEN
from plugins import genre_list

# Initialize IMDbPY
ia = IMDb()

@Client.on_message(filters.command("search_genre"))
async def search_genre(client, message):
    # Extract the user's query
    genre = message.text.split(" ", 1)[1]

    # Search for movies by genre using IMDbPY
    movies = ia.get_keyword(genre)

    # Extract and format the results
    if movies:
        movie_list = "\n".join(movie["title"] for movie in movies)
        response = f"Movies in the {genre} genre:\n{movie_list}"
    else:
        response = f"No movies found in the {genre} genre."

    # Send the response to the user
    await message.reply(response)

