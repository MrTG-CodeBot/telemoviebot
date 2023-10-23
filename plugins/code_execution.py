from pyrogram import Client, filters
import subprocess
import re
import os
import shlex
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter
from tinydb import TinyDB, Query
import psutil  # Import psutil for system information
from info import ADMINS, AUTHORIZED_GROUPS
from database import users_chats_db

AUTHORIZED_GROUPS = [-1001579748507]

# Supported programming languages
languages = {
    "python": "python",
    "javascript": "nodejs",
    "ruby": "ruby",
    "java": "java",
    "c": "gcc -o code -x c -",  # C language (compile and run)
    "cpp": "g++ -o code -x c++ -",  # C++ language (compile and run)
    "go": "go run",  # Go language
    "php": "php",  # PHP language
    "perl": "perl",  # Perl language
    # Add more languages as needed
}

# Initialize the database
db = TinyDB('db.json')

# Define a command to execute code
@Client.on_message(filters.command("run") & filters.chat(AUTHORIZED_GROUPS))
def execute_code(client, message):
    try:
        # Extract the code and language from the message
        parts = shlex.split(message.text)
        if len(parts) < 3 or parts[1].lower() not in languages:
            message.reply_text("Usage: /run [language] [code]")
            return
        language = languages[parts[1].lower()]
        code = " ".join(parts[2:])

        # Validate and sanitize input code
        if not re.match(r"^[a-zA-Z0-9_!@#\$%^&*()_\-+=\[\]{};:'\",.<>/\|?~`\\ \b\n\n]*$",code):
            raise Exception("Invalid characters in code")

        # Create a unique filename for the code
        filename = f"code_{message.chat.id}_{language.replace(' ', '_')}.txt"

        # Write the code to a temporary file
        with open(filename, "w") as code_file:
            code_file.write(code)

        # Execute the code with a time limit
        cmd = f"{language} {filename}"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result, error = process.communicate(timeout=10)
        os.remove(filename)  # Clean up the temporary file

        # Check for errors and return the result
        if process.returncode == 0:
            # Send the result with syntax highlighting
            lexer = get_lexer_by_name(language, stripall=True)
            formatter = TerminalFormatter()
            result_highlighted = highlight(result, lexer, formatter)
            message.reply_text(result_highlighted)
        else:
            message.reply_text(f"An error occurred: {error}")

        # Store the code and result in the database
        user_id = message.from_user.id
        db.insert({"user_id": user_id, "code": code, "result": result})

    except subprocess.TimeoutExpired:
        message.reply_text("**Code execution timed out.**")
    except Exception as e:
        message.reply_text(f"**An error occurred: {str(e)}**")

# Define a command to retrieve previous code and results
@Client.on_message(filters.command("my_history") & filters.chat(AUTHORIZED_GROUPS))
def retrieve_history(client, message):
    user_id = message.from_user.id
    results = db.search(Query().user_id == user_id)
    if results:
        message.reply_text("Your code execution history:\n")
        for entry in results:
            code = entry.get("code")
            result = entry.get("result")
            message.reply_text(f"Code:\n{code}\nResult:\n{result}\n")
    else:
        message.reply_text("**No code execution history found for you.**")

# Bot Status command
@Client.on_message(filters.command("sakura"))
def bot_status(client, message):
    uptime = str(psutil.boot_time())
    bot_info = f"**Bot Uptime: {uptime}\n**"
    bot_info += f"**CPU Usage: {psutil.cpu_percent(interval=1)}%\n**"
    bot_info += f"**RAM Usage: {psutil.virtual_memory().percent}%**"
    message.reply_text(bot_info)

