import pyrogram
from pyrogram import Client, InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("rename") & filters.document)
def rename_document(client, message):
    file_id = message.document.file_id
    file_name = message.document.file_name

    # Create an inline keyboard with two buttons: "Rename" and "Cancel"
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("Rename", callback_data=f"rename_{file_id}"),
            InlineKeyboardButton("Cancel", callback_data="cancel"),
        ]]
    )

    # Send the inline keyboard to the user
    message.reply_text("Select an option:", reply_markup=keyboard)

@Client.on_callback_query(filters.regex(r"^rename_\d+$"))
def handle_rename_callback(client, callback_query):
    file_id = int(callback_query.data.split("_")[1])

# Get the current file name
    current_filename = document.file_name

    # Ask the user for the new file name
    await message.reply_text(f"Current file name: {current_filename}")

    # Ask the user for the new file name
    message = callback_query.message.edit_text("Enter the new file name:")

    # Wait for the user to reply with the new file name
@Client.on_message(filters.from_user(callback_query.from_user.id))
def handle_new_file_name(client, message):
        new_file_name = message.text

        # Try to rename the file
        try:
            client.download_media(file_id, file_name=new_file_name)
            message.reply_text(f"File renamed to {new_file_name}")
        except Exception as e:
            message.reply_text(f"Failed to rename file: {e}")

        # Remove the inline keyboard
        callback_query.message.edit_text("File renamed")

