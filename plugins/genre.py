from pyrogram import Client, filters
from imdb import IMDb
from info import API_ID, API_HASH, BOT_TOKEN
import requests

# Initialize IMDbPY
ia = IMDb()

# Define a function to get the image URL for a movie
def get_movie_image_url(movie_id):
  movie = ia.get_movie(movie_id)
  image_url = movie.get("cover")
  return image_url

# Define a function to send a message with an image
async def send_message_with_image(client, message, image_url):
  await message.reply_photo(image_url, caption=message.text)

@Client.on_message(filters.command("search_genre"))
async def search_genre(client, message):
  """
  Search for movies by genre using IMDbPY and send the results to the user with images.

  Args:
    client (pyrogram.Client): The PyroGram client.
    message (pyrogram.Message): The message to be handled.
  """

  # Extract the user's query
  genre = message.text.split(" ", 1)[1]

  # Search for movies by genre using IMDbPY
  movies = ia.get_keyword(genre)

  # Create a list to store the movie image URLs
  movie_image_urls = []

  # Iterate over the movies and get the image URL for each movie
  for movie in movies:
    movie_image_url = get_movie_image_url(movie["id"])
    movie_image_urls.append(movie_image_url)

  # Format the response
  response = f"**Movies in the {genre} genre:**\n"

  # Iterate over the movie image URLs and send a message with an image for each movie
  for movie_image_url in movie_image_urls:
    await send_message_with_image(client, message, movie_image_url)

  # If no movies were found, send a message to the user
  if not movies:
    response = f"**No movies found in the {genre} genre.**"

  # Send the final response to the user
  await message.reply(response)
