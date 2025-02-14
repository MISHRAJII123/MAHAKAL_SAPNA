from AnonXMusic import app
from pyrogram.errors import RPCError, UserAlreadyParticipant, ChatAdminRequired, InviteRequestSent, UserNotParticipant
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton, Message, ChatJoinRequest
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode, ChatMemberStatus
from logging import getLogger
from AnonXMusic.utils.database import add_served_chat, get_assistant, is_active_chat
from AnonXMusic.misc import SUDOERS
import asyncio
import random
import os

LOGGER = getLogger(__name__)

class WelDatabase:
    def __init__(self):
        self.data = {}

    async def find_one(self, chat_id):
        return chat_id in self.data

    async def add_wlcm(self, chat_id):
        if chat_id not in self.data:
            self.data[chat_id] = {"state": "on"}  # Default state is "on"

    async def rm_wlcm(self, chat_id):
        if chat_id in self.data:
            del self.data[chat_id]

wlcm = WelDatabase()

class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None

@app.on_message(filters.command("welcome") & ~filters.private)
async def auto_state(_, message):
    usage = "**ᴜsᴀɢᴇ:**\n**⦿ /welcome [on|off]**"
    if len(message.command) == 1:
        return await message.reply_text(usage)
    
    chat_id = message.chat.id
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        A = await wlcm.find_one(chat_id)
        state = message.text.split(None, 1)[1].strip().lower()
        
        if state == "off":
            if A:
                await message.reply_text("**ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ !**")
            else:
                await wlcm.add_wlcm(chat_id)
                await message.reply_text(f"**ᴅɪsᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ɪɴ** {message.chat.title}")
        
        elif state == "on":
            if not A:
                await wlcm.add_wlcm(chat_id)  # Corrected from rm_wlcm to add_wlcm for "on"
                await message.reply_text(f"**ᴇɴᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ɪɴ** {message.chat.title}")
        else:
            await message.reply_text(usage)
    else:
        await message.reply("**sᴏʀʀʏ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴇɴᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ!**")

@app.on_chat_member_updated(filters.group, group=-3)
async def greet_new_member(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    count = await app.get_chat_members_count(chat_id)
    A = await wlcm.find_one(chat_id)

    # If the welcome message is disabled for the chat, do nothing
    if A:
        return

    user = None
    if member.new_chat_member:
        user = member.new_chat_member.user
    elif member.old_chat_member:
        user = member.old_chat_member.user
    
    if not user:
        return  # Exit if no user found in the update
    
    try:
        # Welcome message
        welcome_message = f"🤍𝗛꯭ᴀ꯭ʀ꯭ʜ꯭ᴀ꯭ʀ꯭ 𝛭꯭ᴀ꯭ʜ꯭ᴀ꯭ᴅ꯭ᴇ꯭ᴠ꯭🤍 {user.mention}, 🤍𝗪꯭ᴇ꯭ʟ꯭ᴄ꯭ᴏ꯭ᴍ꯭ᴇ꯭᪳🤍 {member.chat.title}!\n\n🤍𝗗꯭ᴍ꯭ 𝗡꯭ᴀ꯭ 𝗞꯭ᴀ꯭ʀ꯭ᴇ꯭🤍\n\n🤍𝗗꯭ᴏ꯭ɴ꯭'ᴛ꯭ 𝗦꯭ᴇ꯭ɴ꯭ᴅ꯭  𝛥꯭ᴅ꯭ᴜ꯭ʟ꯭ᴛ꯭ 𝗦꯭ᴛ꯭ᴀ꯭ғ꯭ғ꯭🤍\n\n🤍𝗙꯭ɪ꯭ɢ꯭ʜ꯭ᴛ꯭ɪ꯭ɴ꯭ɢ꯭ 𝗗꯭ᴍ꯭ 𝗡꯭ᴏ꯭ᴛ꯭ 𝛥꯭ʟ꯭ʟ꯭ᴏ꯭ᴡ꯭ᴇ꯭ᴅ꯭🤍\n\n🤍𝗣꯭ʟ꯭ᴇ꯭ᴀ꯭ꜱ꯭ᴇ꯭ Rᴇ꯭ꜱ꯭ᴘ꯭ᴇ꯭ᴄ꯭ᴛ꯭ 𝛯꯭ᴠ꯭ᴇ꯭ʀ꯭ʏ꯭ᴏ꯭ɴ꯭ᴇ꯭🤍\n\n🤍𝛭꯭ᴜ꯭ᴛ꯭ᴇ꯭/ʙ꯭ᴀ꯭ɴ꯭ 𝛥꯭ʙ꯭ᴜ꯭ꜱ꯭ᴇ꯭=🤍\n\n \ • 🤍𝛥꯭ᴀ꯭ᴏ꯭ 𝗧꯭ᴏ꯭🤍᪳𝛭꯭ᴏ꯭ꜱ꯭ᴛ꯭ 𝗪꯭ᴇ꯭ʟ꯭ᴄ꯭ᴏ꯭ᴍ꯭ᴇ꯭🤍\n\n🤍𝗝꯭ᴀ꯭ᴏ꯭ 𝗧꯭ᴏ꯭🤍𝗕꯭ʜ꯭ᴇ꯭ᴇ꯭ᴅ꯭ 𝗞꯭ᴀ꯭ᴍ꯭🤍᪳!\n\────────────────────\n" \fᴛ ᴏ ᴛ ᴀ ʟ ᴍ ᴇ ᴍ ʙ ᴇ ʀ: {count}\n \n────────────────────**"
        
        # Creating an inline button to "Join 👋" with the link
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Join 👋", url="https://t.me/+olg0fMkm9VQ3NzY9")]]
        )

        # Send the welcome message with the inline button
        await app.send_message(chat_id, welcome_message, reply_markup=keyboard)
    except Exception as e:
        LOGGER.error(f"Error sending welcome message: {e}")
