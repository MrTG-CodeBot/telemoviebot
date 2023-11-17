import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Script import script
from info import API_ID, API_HASH, BOT_TOKEN

# Define the command handler
@Client.on_message(filters.command("about") & filters.incoming & filters.private)
async def about(client, message):
    await message.reply(ABOUT_TXT)
   buttons = [
            [
                InlineKeyboardButton('<^ ~ ^> ᴍʀ.ʙᴏᴛ ᵀᴳ </>', url="https://t.me/MrTG_Coder"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
