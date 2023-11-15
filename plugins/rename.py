import os
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
import asyncio
from info import API_ID, API_HASH, BOT_TOKEN
import tqdm

@Client.on_message(pyrogram.filters.command("rename") & pyrogram.filters.document)
async def rename_document(client, message):
    file_id = message.document.file_id
    file_name = message.document.file_name

    # Check if the file size is less than 2 GB
    if message.document.file_size > 2097152000:
        await message.reply_text("Sorry, files larger than 2 GB cannot be renamed.")
        return

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("Rename", callback_data=f"rename_{file_id}"),
            InlineKeyboardButton("Cancel", callback_data="cancel"),
        ]]
    )

    # Send the inline keyboard to the user
    message = await message.reply_text("Select an option:", reply_markup=keyboard)

@Client.on_callback_query(pyrogram.filters.regex(r"^rename_\d+$"))
async def handle_rename_callback(client, callback_query):
    file_id = int(callback_query.data.split("_")[1])

    # Get the current file name
    current_filename = await client.get_file_info(file_id).file_name

    # Send a message to the user with the current file name
    await callback_query.message.edit_text(f"Current file name: {current_filename}")

    # Send a message to the user asking for the new file name
    message = await callback_query.message.edit_text("Enter the new file name:")

@Client.on_message(pyrogram.filters.from_user(callback_query.from_user.id))
async def handle_new_file_name(client, message):
        new_file_name = message.text

        # Download the file from Telegram with progress bar
        total_size = message.document.file_size
        with tqdm.tqdm(total=total_size) as pbar:
            try:
                document = await client.download_media(file_id, progress_callback=lambda x: pbar.update(x))
            except FloodWaitError as e:
                await asyncio.sleep(e.x)
                document = await client.download_media(file_id, progress_callback=lambda x: pbar.update(x))

        # Rename the downloaded file
        try:
            os.rename(document.file_name, new_file_name)

            # Upload the renamed file to Telegram with progress bar
            total_size = os.path.getsize(new_file_name)
            with tqdm.tqdm(total=total_size) as pbar:
                await client.send_document(message.chat.id, new_file_name, caption=f"File renamed to {new_file_name}", progress_callback=lambda x: pbar.update(x))

            # Delete the downloaded file
            os.remove(new_file_name)

            # Edit the message to inform the user that the file has been renamed
            await callback_query.message.edit_text(f"File renamed to {new_file_name}", reply_markup=None)
        except Exception as e:
            await callback_query.message.edit_text(f"Failed to rename file: {e}", reply_markup=None)

@Client.on_message(pyrogram.filters.command("re_help"))
async def help_command(client, message):
    help_text = """
    Here are the commands you can use:
    /rename: Rename a document. Reply to a document with /rename to use this command.
    """
    await message.reply_text(help_text)
