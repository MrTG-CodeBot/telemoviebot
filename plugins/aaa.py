from pyrogram import Client, filters

@Client.on_message(filters.command("clone") & filters.private)
async def clone(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a username to clone.")
        return

    username_to_clone = message.command[1]
    await message.reply_text(f"Cloning {username_to_clone}...")

    try:
        user = await app.get_users(username_to_clone)
        await message.reply_text(f"Successfully cloned {user.username}!")
    except Exception as e:
        await message.reply_text(f"Error: {e}")
