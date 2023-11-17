import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Script import script
from info import API_ID, API_HASH, BOT_TOKEN

 ABOUT_TXT ="""<b>✯ Mʏ ɴᴀᴍᴇ: {}
✯ Dᴇᴠᴇʟᴏᴩᴇʀ: <a href=https://t.me/Unni0240>ᴍʀ.ʙᴏᴛ ᴛɢ</a>
✯ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a>
✯ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 3</a>
✯ Mʏ DᴀᴛᴀBᴀꜱᴇ: ᴍᴏɴɢᴏ-ᴅʙ
✯ Mʏ Sᴇʀᴠᴇʀ: ʀᴇɴᴅᴇʀ
✯ ᴠᴇʀꜱɪᴏɴ: {__version__}"""

# Define the command handler
@Client.on_message(filters.command("about") & filters.incoming & filters.private)
async def about(client, message):
    await message.reply(ABOUT_TXT)
    buttons = [[
            InlineKeyboardButton('<^ ~ ^> ᴍʀ.ʙᴏᴛ ᵀᴳ </>', url="https://t.me/MrTG_Coder")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text("<b>Hᴇʟʟᴏ {}.\nMʏ Nᴀᴍᴇ Is <a href=https://t.me/{}>{}</a>.\nI Cᴀɴ Pʀᴏᴠɪᴅᴇ Mᴏᴠɪᴇ Fᴏʀ Yᴏᴜ Jᴜsᴛ Aᴅᴅ Mᴇ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ Oʀ Jᴏɪɴ Oᴜʀ Gʀᴏᴜᴘ</b>", reply_markup=reply_markup)
