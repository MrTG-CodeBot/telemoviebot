import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message
from info import API_ID, API_HASH, BOT_TOKEN

async def download_reel(reel_url):
    async with client.session() as session:
        async with session.get(reel_url) as response:
            reel_data = await response.read()

        with open("reel.mp4", "wb") as f:
            f.write(reel_data)

        return "reel.mp4"
      
@Client.on_message(filters.command("reel"))
async def reel_handler(client: Client, message: Message):
    reel_url = message.text.split()[1]

    try:
        reel_path = await download_reel(reel_url)

        await client.send_document(message.chat.id, reel_path, caption="Your Reel is ready!")
    except Exception as e:
        await client.send_message(message.chat.id, f"Failed to download Reel: {e}")
