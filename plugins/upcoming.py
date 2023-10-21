import os
import datetime
from pyrogram import Client, filters
import requests
from info import TMDB_API_KEY

# Define the /upcomingmovies command to show upcoming movie releases
@Client.on_message(filters.command("upcoming_movies"))
async def upcoming_movies(_, message):
    # Fetch upcoming movies from TMDb API
    upcoming_movies = get_upcoming_movies()
    
    if upcoming_movies:
        # Generate a message with upcoming movie details
        message_text = "Upcoming Movie Releases:\n"
        for movie in upcoming_movies:
            message_text += f"{movie['title']} - {movie['release_date']}\n"
        
        await message.reply_text(message_text)
    else:
        await message.reply_text("No upcoming movies found.")

# Function to get upcoming movies using TMDb API
def get_upcoming_movies():
    base_url = "https://api.themoviedb.org/3/movie/upcoming"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "region": "US"  # Adjust the region as needed
    }

url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiMGQ1OGRjZDBjY2JlMTkzNDBhYTE0M2RhZjRjNmFkMCIsInN1YiI6IjY1MzM4ODJjOTFmMGVhMDBjNDIyMTk0NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.dG-TfbI8hwDlXJwSVqPh86pzrVycmkeKrWL6a3g1q6s"
}    
   today = datetime.date.today()
    next_month = today + datetime.timedelta(days=30)  # Get movies for the next 30 days

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        upcoming_movies = [movie for movie in data["results"] if movie["release_date"] >= str(today) and movie["release_date"] <= str(next_month)]
        return upcoming_movies
    return []


