from pyrogram import Client, filters

@app.on_message(filters.command("clone") & filters.private)
async def clone(client, message):
    if len(message.command) < 2:
        await message.reply_text("<b>Adding soon or not</b>.")
