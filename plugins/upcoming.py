import datetime
from pyrogram import Client, filters
import requests
from info import TMDB_API_KEY

# Define the /upcomingmovies command to show upcoming movie releases
@app.on_message(filters.command("upcoming_movies"))
async def upcoming_movies(_, message):
    # Fetch upcoming movies from TMDb API for a selected region
    selected_region = "United States"  # Replace with the desired region
    upcoming_movies = get_upcoming_movies(selected_region)
    
    if upcoming_movies:
        # Generate a message with upcoming movie details
        message_text = f"Upcoming Movie Releases in {selected_region}:\n"
        for movie in upcoming_movies:
            message_text += f"{movie['title']} - {movie['release_date']}\n"
        
        await message.reply_text(message_text)
    else:
        await message.reply_text(f"No upcoming movies found in {selected_region}.")

# Function to get upcoming movies using TMDb API for a selected region
def get_upcoming_movies(selected_region):
    # Map the selected region to its TMDb region code
    regions = {
        "United States": "US",
        "United Kingdom": "GB",
        "Canada": "CA",
        "Australia": "AU",
        "India": "IN",
        "Germany": "DE",
        "France": "FR",
        "Japan": "JP",
    }

    if selected_region in regions:
        tmdb_region_code = regions[selected_region]
    else:
        return []  # Return an empty list if the region is not found in the mapping

    base_url = "https://api.themoviedb.org/3/movie/upcoming"
    params = {
        "api_key": tmdb_api_key,
        "language": "en-US",
        "region": tmdb_region_code
    }

    today = datetime.date.today()
    next_month = today + datetime.timedelta(days=30)  # Get movies for the next 30 days

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        upcoming_movies = [movie for movie in data["results"] if movie["release_date"] >= str(today) and movie["release_date"] <= str(next_month)]
        return upcoming_movies
    return []
