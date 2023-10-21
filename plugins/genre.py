from pyrogram import Client, filters
from imdb import IMDb
from info import API_ID, API_HASH, BOT_TOKEN,TMDB_API_KEY

# Initialize IMDbPY
ia = IMDb()

@Client.on_message(filters.command("search_genre"))
async def search_genre(client, message):
    # Extract the user's query
    user_input = message.text.split(" ", 1)[1]

    # Check if the user's input matches a valid genre
    genre = None
    if query in movie_genres:
        if user_input.lower() in valid_genre.lower():
            genre = valid_genre
            break

    if genre:
        # Search for movies by genre using IMDbPY
        movies = ia.get_keyword(genre)

        # Extract and format the results
        if movies:
            movie_list = "\n".join(movie["title"] for movie in movies)
            response = f"Movies in the {genre} genre:\n{movie_list}"
        else:
            response = f"No movies found in the {genre} genre."
    else:
        response = "Invalid genre. Please choose from the following genres:\n" + "\n".join(movie_genres)

    # Send the response to the user
    await message.reply(response)
