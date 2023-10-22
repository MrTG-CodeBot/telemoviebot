from pyrogram import Client, filters
import subprocess
import re

# Authorized users or groups
authorized_users = [1342641151, -1002032624737]  # Add user or group IDs

# Define a command to execute code
@Client.on_message(filters.command("run") & filters.user(authorized_users))
def execute_code(client, message):
    try:
        # Extract the code from the message
        code = message.text.split(" ", 1)[1]
        
        # Validate and sanitize input code
        if not re.match(r"^[a-zA-Z0-9_\s]*$", code):
            raise Exception("**Invalid characters in code**")

        # Execute the code with a time limit
        result = subprocess.check_output(code, shell=True, text=True, timeout=10)

        # Send the result with syntax highlighting
        message.reply_code(result, "python")
    except subprocess.TimeoutExpired:
        message.reply_text("Code execution timed out.")
    except Exception as e:
        message.reply_text(f"An error occurred: {str(e)}")

