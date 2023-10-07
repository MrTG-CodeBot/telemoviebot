from pyrogram import Client
from pyrogram.types import Message

async def start_handler(client: Client, message: Message):
    await message.reply("Welcome! This is the start command handler.")

# You can define other handlers specific to the start command if needed.
