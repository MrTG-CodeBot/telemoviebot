import logging
import pyrogram
from pyrogram import Client, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWaitError
import asyncio
from info import API_ID, API_HASH, BOT_TOKEN
import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@Client.on_message(pyro.filters.command("rename") & pyro.filters.document)
async def rename_document(client, message):
    try:
        file_id = message.document.file_id
        file_name = message.document.file_name

        logging.info(f"Initiating file rename for file_id: {file_id}, file_name: {file_name}")

        # Check if the file size is less than 2 GB
        if message.document.file_size > 2097152000:
            await message.reply_text("Sorry, files larger than 2 GB cannot be renamed.")
            return

        # Create inline keyboard
        keyboard = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("Rename", callback_data=f"rename_{file_id}"),
                InlineKeyboardButton("Cancel", callback_data="cancel"),
            ]]
        )

        # Send inline keyboard to the user
        message = await message.reply_text("Select an option:", reply_markup=keyboard)
    except Exception as e:
        logging.error(f"Error during file rename initiation: {e}")
        await message.reply_text(f"Failed to initiate file rename: {e}")

@Client.on_callback_query(pyro.filters.regex(r"^rename_\d+$"))
async def handle_rename_callback(client, callback_query):
    try:
        file_id = int(callback_query.data.split("_")[1])

        # Get current file name
        current_filename = await client.get_file_info(file_id).file_name

        # Send message with current file name
        await callback_query.message.edit_text(f"Current file name: {current_filename}")

        # Send message asking for new file name
        message = await callback_query.message.edit_text("Enter the new file name:")
    except Exception as e:
        logging.error(f"Error during handling rename callback: {e}")
        await callback_query.message.edit_text(f"Failed to handle rename callback: {e}")

@Client.on_message(pyro.filters.chat(callback_query.from_user.chat.id) & pyro.filters.from_user(callback_query.from_user.id))
async def handle_new_file_name(client, message):
    try:
        new_file_name = message.text

        # Download file with progress bar
        total_size = message.document.file_size
        with tqdm.tqdm(total=total_size) as pbar:
            try:
                document = await client.download_media(file_id, progress_callback=lambda x: pbar.update(x))
            except FloodWaitError as e:
                logging.warning(f"FloodWaitError during file download: {e}")
                await asyncio.sleep(e.x)
                document = await client.download_media(file_id, progress_callback=lambda x: pbar.update(x))

        # Rename downloaded file
        try:
            os.rename(document.file_name, new_file_name)

            # Upload renamed file with progress bar
            total_size = os.path.getsize(new_file_name)
            with tqdm.tqdm(total=total_size) as pbar:
                await app.send_document(message.chat.id, new_file_name, caption=f"File renamed to {new_file_name}", progress_callback=lambda x: pbar.update(x))

            # Delete downloaded file
            os.remove(new_file_name)

            # Edit message to inform user of successful renaming
            await callback_query.message.edit_text(f"File renamed to {new_file_name}", reply_markup=None)
        except Exception as e:
            logging.error(f"Failed to rename file: {e}")  
