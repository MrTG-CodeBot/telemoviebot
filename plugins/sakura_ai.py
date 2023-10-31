import pyrogram
from pyrogram import Client
from bard import Bard
from info import API_ID, API_HASH, BOT_TOKEN, BARD_AI_API_KEY

# Create a new Bard AI instance.
bard = Bard(api_key="YOUR_BARD_AI_API_KEY")

# Create a new Telegram bot client.
Client("sakura_ai")

# Define a function that will be called when the bot receives the `/sakura_ai` command.
async def sakura_ai_command(client: Client, message: pyrogram.types.Message):
    """Command handler for the `/sakura_ai` command."""

    # Get the user's query.
    query = message.text.split(" ")[1]

    # Generate a response from Bard AI.
    response = bard.generate_response(query)

    # Send the response to the user.
    await message.reply_text(response)

# Register the command handler with the Telegram bot client.
Client.add_handler(sakura_ai_command)

