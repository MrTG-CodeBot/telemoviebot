from pyrogram import Client
from pyrogram.handlers import MessageHandler
import signal
import config  # Import your configuration

from composer import composer  # Import your composer from modules

# Create a Pyrogram Client instance
bot = Client("my_bot", bot_token=config.BOT_TOKEN)

# Function to stop the bot gracefully on signals
def stop_bot(signum, frame):
    print("Stopping the bot...")
    bot.stop()
    print("Bot stopped.")
    exit(0)

# Set up signal listeners for graceful bot shutdown
signal.signal(signal.SIGINT, stop_bot)
signal.signal(signal.SIGTERM, stop_bot)

# Set up message handler to use the composer
@bot.on_message()
async def message_handler(client, message):
    await composer.handle(message)

# Start the bot
if __name__ == "__main__":
    bot.start()
