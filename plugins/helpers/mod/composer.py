from pyrogram import Client
from pyrogram import filters

from start import start_handler
from cloner import cloner_handler

app = Client("my_bot")

@app.on_message(filters.command("start"))
async def start_command_handler(client: Client, message: Message):
    await start_handler(client, message)

@app.on_message(filters.command("cloner"))
async def cloner_command_handler(client: Client, message: Message):
    await cloner_handler(client, message)

if __name__ == "__main__":
    app.run()
