from pyrogram import Client, filters
import requests
import os
from info import API_ID,API_ID,BOT_TOKEN

# Create a new Pyrogram client
Client("my_bot")

# Define the command handler for the '/start' command
@Client.on_message(filters.command("start"))
def start_command(client, message):
    # Send a welcome message to the user
    message.reply_text("Welcome to the Instagram Reels Downloader Bot!")

# Define the command handler for the '/download' command
@Client.on_message(filters.command("download"))
def download_command(client, message):
    # Get the Instagram Reels URL from the command arguments
    url = message.text.split(" ")[1]

    try:
        # Send a message to inform the user that the download is in progress
        progress_message = message.reply_text("Downloading...")

        # Get the video URL by making a request to Instagram
        response = requests.get(url)
        if response.status_code == 200:
            # Create a filename based on the timestamp
            filename = f"reels_{int(time.time())}.mp4"
            
            # Save the video content to a file
            with open(filename, "wb") as file:
                file.write(response.content)
            
            # Send the downloaded video to the user
            message.reply_document(document=filename)
            
            # Clean up the temporary file
            os.remove(filename)

            # Inform the user that the download is complete
            progress_message.edit_text("Download complete!")
        else:
            progress_message.edit_text("Error: Unable to download the Reels.")
    except Exception as e:
        progress_message.edit_text(f"An error occurred: {str(e)}")

# Start the client
app.run()
