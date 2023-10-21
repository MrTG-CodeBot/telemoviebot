import datetime
from pyrogram import Client, filters
import requests
from info import TMDB_API_KEY

# Define the /upcoming_movies command to show upcoming movie releases
@Client.on_message(filters.command("upcoming_movies"))
async def upcoming_movies(client, message):
    # Parse the region from the user's command, e.g., "/upcoming_movies United States"
    command_parts = message.text.split()
    if len(command_parts) > 1:
        selected_region = " ".join(command_parts[1:])
    else:
        selected_region = "India"  # Default to United States if no region is specified

    # Fetch upcoming movies for the selected region
    upcoming_movies = get_upcoming_movies(selected_region)

    if upcoming_movies:
        # Paginate the movie list (display up to 10 movies per page)
        page_size = 10
        current_page = 1
        total_pages = (len(upcoming_movies) + page_size - 1) // page_size

        while current_page <= total_pages:
            start_idx = (current_page - 1) * page_size
            end_idx = current_page * page_size
            page_movies = upcoming_movies[start_idx:end_idx]

            # Generate a message with upcoming movie details for the current page
            message_text = f"Upcoming Movie Releases in {selected_region} (Page {current_page}/{total_pages}):\n"
            for movie in page_movies:
                formatted_date = format_date(movie['release_date'])
                message_text += f"{movie['title']} - {formatted_date}\n\n"

            # Send the message for the current page
            await message.reply_text(message_text)

            current_page += 1
    else:
        await message.reply_text(f"No upcoming movies found in {selected_region}.")

# Function to get upcoming movies using TMDb API for a selected region
def get_upcoming_movies(selected_region):
    base_url = "https://api.themoviedb.org/3/movie/upcoming?api_key=b0d58dcd0ccbe19340aa143daf4c6ad0"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-IN",  # Adjust the language code as needed
        "region": get_region_code(selected_region)
    }

    today = datetime.date.today()
    next_month = today + datetime.timedelta(days=30)  # Get movies for the next 30 days

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        upcoming_movies = [movie for movie in data["results"] if movie["release_date"] >= str(today) and movie["release_date"] <= str(next_month)]
        return upcoming_movies
    return []

# Function to format the date in a user-friendly way (e.g., "January 1, 2023")
def format_date(date_str):
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date.strftime("%B %d, %Y")

# Function to get the TMDb region code based on the selected region name
def get_region_code(selected_region):
    # Define a mapping of region names to TMDb region codes
    region_mapping = {
        "United States": "US",
        "United Kingdom": "GB",
        "Canada": "CA",
        "Australia": "AU",
        "India": "IN",
        "Germany": "DE",
        "France": "FR",
        "Japan": "JP",
    }

    # Default to "US" if the selected region is not in the mapping
    return region_mapping.get(selected_region, "IN")
