from pyrogram import Client, filters
from pyrogram.types import Message

# Import your command handlers
from start import start_handler
from clone import cloner_handler

app = Client("my_bot")

# Create a Composer instance
composer = filters.create()

# Add command handlers to the Composer
composer.command("start")(start_handler)
composer.command("cloner")(cloner_handler)

# Register the Composer with the bot
app.add_handler(composer)

if __name__ == "__main__":
    app.run()
