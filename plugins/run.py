import pyrogram
from pyrogram import filters, Client
import subprocess
from info import API_ID, API_HASH, BOT_TOKEN

# Define a filter to capture messages with code
code_filter = filters.text & filters.private

# Command handler to execute Python code
@Client.on_message(code_filter & filters.command("run", prefixes="/"))
async def run_code(client, message):
    code = message.text.split(" ", 1)[1]
    
    try:
        # Execute the Python code using subprocess
        result = subprocess.check_output(["python", "-c", code], stderr=subprocess.STDOUT, text=True, timeout=10)
        
        # Send the result back to the user
        await message.reply(f"Output:\n{result}")
    except subprocess.CalledProcessError as e:
        # Handle errors and exceptions
        await message.reply(f"Error:\n{e.output}")
    except subprocess.TimeoutExpired:
        # Handle code execution timeout
        await message.reply("Code execution timed out.")
    except Exception as e:
        # Handle other exceptions
        await message.reply(f"An error occurred: {str(e)}")
