import pyrogram
from pyrogram import Client, filters, types

async def rename_document(message: types.Message):
    # Get the document file from the message
    document = message.document

    # Get the current file name
    current_filename = document.file_name

    # Ask the user for the new file name
    await message.reply_text(f"Current file name: {current_filename}")
    await message.reply_text("Enter the new file name:")

    # Get the new file name from the user
    new_filename = await app.wait_for_message(filters.text)

    # Rename the file
    await app.download_media(document.file_id, file_name=new_filename)

    # Send a message to the user indicating that the file has been renamed
    await message.reply_text(f"File renamed to: {new_filename}")

# Define a command handler for the `/rename_document` command
@Client.on_message(filters.command("rename_document"))
async def handle_rename_document_command(message: types.Message):
    if not message.reply_to_message:
        await message.reply_text("Please reply to a document file to rename it.")
        return

    # Check if the replied message is a document file
    if message.reply_to_message.document:
        await rename_document(message.reply_to_message)
    else:
        await message.reply_text("Please reply to a document file to rename it.")
