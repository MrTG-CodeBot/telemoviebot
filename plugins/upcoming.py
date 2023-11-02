import datetime
from pyrogram import Client, filters
import requests
from info import TMDB_API_KEY

# Define a new command parameter to specify multiple regions
parser = argparse.ArgumentParser()
parser.add_argument("--regions", nargs="*", help="Comma-separated list of regions")

# Define a new command parameter to specify the sorting option
parser.add_argument("--sort", choices=["release_date", "popularity", "rating"], help="Sort order for the list of upcoming movies")

# Define a new command parameter to specify the filtering criteria
parser.add_argument("--genre", choices=["Action", "Adventure", "Comedy", "Drama", "Horror", "Sci-Fi"], help="Filter by genre")
parser.add_argument("--language", choices=["English", "Hindi", "Tamil", "Telugu", "Malayalam"], help="Filter by language")

# Define a new command parameter for pagination
parser.add_argument("--page", type=int, help="Page number for the list of upcoming movies")

# Parse the command-line arguments
args = parser.parse_args()

# Get the upcoming movies for the specified regions
def get_upcoming_movies(regions):
    base_url = "https://api.themoviedb.org/3/movie/upcoming"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "EN_IN" 
    }

    for region in regions:
        params["region"] = get_region_code(region)
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            upcoming_movies = [movie for movie in data["results"]]
        else:
            print(f"Could not fetch upcoming movies for region: {region}")

    return upcoming_movies

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

# Define the /upcoming_movies command to show upcoming movie releases
@Client.on_message(filters.command("upcoming_movies"))
async def upcoming_movies(client, message):
    # Get the upcoming movies for the specified regions
    upcoming_movies = get_upcoming_movies(args.regions if args.regions else ["India"])

    # Sort the list of movies based on the specified sorting option
    if args.sort:
        upcoming_movies.sort(key=lambda movie: movie[args.sort], reverse=True)

    # Filter the list of movies based on the specified filtering criteria
    if args.genre:
        upcoming_movies = [movie for movie in upcoming_movies if movie["genre"] == args.genre]
    if args.language:
        upcoming_movies = [movie for movie in upcoming_movies if movie["language"] == args.language]

    # Paginate the list of movies (display up to 10 movies per page)
    page_size = 10
    current_page = args.page if args.page else 1
    total_pages = (len(upcoming_movies) + page_size - 1) // page_size

    while current_page <= total_pages:
        start_idx = (current_page - 1) * page_size
        end_idx = current_page * page_size
        page_movies = upcoming_movies[start_idx:end_idx]

        # Generate a message with upcoming movie details for the current page
        message_text = f"Upcoming Movie
