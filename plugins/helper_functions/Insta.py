from pyrogram import Client, filters
import os
import time
import requests  # Add this import

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text("Welcome to the Instagram Reels Downloader Bot!")

@app.on_message(filters.command("download"))
def download_command(client, message):
    url = message.text.split(" ")[1]

    try:
        progress_message = message.reply_text("Downloading...")

        response = requests.get(url)
        if response.status_code == 200:
            filename = f"reels_{int(time.time())}.mp4"
            
            with open(filename, "wb") as file:
                file.write(response.content)
            
            message.reply_document(document=filename)
            
            os.remove(filename)

            progress_message.edit_text("Download complete!")
        else:
            progress_message.edit_text("Error: Unable to download the Reels.")
    except Exception as e:
        progress_message.edit_text(f"An error occurred: {str(e)}")

@app.on_message(filters.command("create"))
def create_command(client, message):
    try:
        progress_message = message.reply_text("Creating Reels...")

        # Add your video creation logic here using a library like MoviePy
        # For example, you can use MoviePy to create a video and save it with a filename

        # Replace the following line with your video creation logic
        # filename = f"reels_{int(time.time())}.mp4"
        
        # Send the created video to the user
        # message.reply_document(document=filename)
        
        # Clean up the temporary file
        # os.remove(filename)

        progress_message.edit_text("Reels creation complete!")
    except Exception as e:
        progress_message.edit_text(f"An error occurred: {str(e)}")

