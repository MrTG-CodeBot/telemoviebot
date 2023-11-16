import pyrogram
import logging
import os
import tqdm
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from info import API_ID, API_HASH, BOT_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Use a list to keep track of ongoing file renames
ongoing_renames = {}

# Define the command handler
@Client.on_message(pyrogram.filters.command("rename") & pyrogram.filters.document)
async def rename_document(client, message):
    file_id = message.document.file_id
    file_name = message.document.file_name

    logging.info(f"Initiating file rename for file_id: {file_id}, file_name: {file_name}")

    if message.document.file_size > 2097152000:
        await message.reply_text("Sorry, files larger than 2 GB cannot be renamed.")
        return

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Rename", callback_data=f"rename_{file_id}"),
                InlineKeyboardButton("Cancel", callback_data="cancel"),
            ]
        ]
    )

    await message.reply_text("Select an option:", reply_markup=keyboard)

# Define the callback query handler
@Client.on_callback_query(pyrogram.filters.regex(r"^rename_\d+$"))
async def handle_rename_callback(client, callback_query):
    file_id = int(callback_query.data.split("_")[1])

    current_filename = await client.get_file_info(file_id).file_name

    await callback_query.message.edit_text(f"Current file name: {current_filename}")

    message = await callback_query.message.edit_text("Enter the new file name:")

# Define the message handler for receiving the new file name
@Client.on_message(pyrogram.filters.text & pyrogram.filters.chat)
async def handle_new_file_name(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user_id in ongoing_renames and chat_id in ongoing_renames[user_id]:
        file_id, current_filename = ongoing_renames[user_id][chat_id]
        new_file_name = message.text

        try:
            total_size = message.document.file_size
            with tqdm.tqdm(total=total_size) as pbar:
                document = await client.download_media(file_id, progress_callback=lambda x: pbar.update(x))
        except FloodWait as e:
            logging.warning(f"FloodWaitError during file download: {e}")
            await asyncio.sleep(e.x)
            document = await client.download_media(file_id, progress_callback=lambda x: pbar.update(x))

        os.rename(document, new_file_name)

        total_size = os.path.getsize(new_file_name)
        with tqdm.tqdm(total=total_size) as pbar:
            await client.send_document(chat_id, new_file_name, caption=f"File renamed to {new_file_name}", progress_callback=lambda x: pbar.update(x))
    else:
        logging.error("File rename not initiated or already completed.")

