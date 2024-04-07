import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.types import Message, ChatPermissions, ChatMember, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ChatInviteLink
import os, asyncio
from pyrogram.errors import UserNotParticipant
from os import environ

F_SUB = int(os.environ.get('F_SUB', '-100xxx'))

@Client.on_message(filters.text & filters.chat(int(-100xxx)))
async def mute_handler(client, message: Message):
    try:
        invite_link = await client.create_chat_invite_link(int(F_SUB))
    except ChatAdminRequired:
        print(f"Make sure Bot is admin in Forcesub channel")
        await message.reply_text(f"Make sure Bot is admin in Forcesub channel")
        return
    if message.text is None:
        return
    else:
        user_id = message.from_user.id
        user = await client.get_chat_member(message.chat.id, message.from_user.id)

        if user.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            return

        x = None

        try:
            x = await client.get_chat_member(F_SUB, user_id)
        except UserNotParticipant:
            pass

        if x and x.status is enums.ChatMemberStatus.MEMBER:
            return

        elif not x or x.status is not enums.ChatMemberStatus.MEMBER:
            await client.restrict_chat_member(
                message.chat.id,
                user_id,
                ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_other_messages=False,
                )
            )
            buttons = [[
                InlineKeyboardButton("join the channel" , url=invite_link.invite_link),
                InlineKeyboardButton("Unmute" , callback_data="unmute"),
                InlineKeyboardButton('close' , callback_data='close')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply_text(
                text=f"Hey{message.from_user.mention}\n you have been muted because you didn't join our f_sub group/channel\n* click the button of <code>join the channel</code>\n*After clicking the button join the channel/group, then back this group and click the unmute button",
                reply_markup=reply_markup)

@Client.on_callback_query()
async def callback_handle(client, query):
    if query.data == 'unmute':
        user_id = query.from_user.id
        try:
            x = await client.get_chat_member(F_SUB, user_id)
            if x.status is enums.ChatMemberStatus.MEMBER:
                await client.restrict_chat_member(
                    message.chat.id,
                    user_id,
                    ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_other_messages=True,
                        can_send_polls=True,
                        can_add_web_page_previews=True,
                        can_change_info=True,
                        can_invite_users=True,
                        can_pin_messages=True
                    )
                )
                buttons = [[InlineKeyboardButton('close', callback_data='close')]]
                reply_markup = InlineKeyboardMarkup(buttons)
                await query.message.edit_text(text="ok unmuted", reply_markup=reply_markup,
                                              parse_mode=enums.ParseMode.HTML)
            else:
                await query.answer("You need to join the channel/group first.", show_alert=True)
        except Exception as e: 
            print(f"Error unmuting user: {e}")
            await query.answer("Something went wrong. Please try again later.", show_alert=True)

    if query.data == 'close':
        await query.message.delete()
        edited_keyboard = InlineKeyboardMarkup([])
        await query.answer()
        await query.message.edit_reply_markup(edited_keyboard)
