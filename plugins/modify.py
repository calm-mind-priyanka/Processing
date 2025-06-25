
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

BOT_OWNER = [6046055058]
user_settings = {}

@Client.on_message(filters.private & filters.command("modify"))
async def modify_command(client, message: Message):
    if message.from_user.id not in BOT_OWNER:
        return await message.reply("🚫 You are not authorized.")
    await settings_menu(client, message)

async def settings_menu(client, message, group_title="YOUR GROUP", group_id="PRIVATE"):
    text = f"""👑 GROUP - {group_title}  
🆔 ID - {group_id}  

SELECT ONE OF THE SETTINGS THAT YOU WANT TO CHANGE ACCORDING TO YOUR GROUP…"""
    btn = [
        [InlineKeyboardButton("👥 FORCE CHANNEL", callback_data="force_channel"),
         InlineKeyboardButton("ℹ️ MAX RESULTS", callback_data="max_results")],
        [InlineKeyboardButton("満 IMDB", callback_data="imdb_toggle"),
         InlineKeyboardButton("🔍 SPELL CHECK", callback_data="spell_toggle")],
        [InlineKeyboardButton("🗑️ AUTO DELETE", callback_data="auto_delete"),
         InlineKeyboardButton("📚 RESULT MODE", callback_data="result_mode")],
        [InlineKeyboardButton("🗂 FILES MODE", callback_data="file_mode"),
         InlineKeyboardButton("📝 FILES CAPTION", callback_data="caption")],
        [InlineKeyboardButton("🥁 TUTORIAL LINK", callback_data="tutorial_link"),
         InlineKeyboardButton("🖇 SET SHORTLINK", callback_data="set_shortner")],
        [InlineKeyboardButton("‼️ CLOSE SETTINGS MENU ‼️", callback_data="close")]
    ]
    await message.reply(text, reply_markup=InlineKeyboardMarkup(btn))

# This file includes the starting setup. Full logic continues in next parts and is assumed to be filled in as discussed.
