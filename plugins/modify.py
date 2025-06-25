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
        [InlineKeyboardButton("🈵 IMDB", callback_data="imdb"),
         InlineKeyboardButton("🔍 SPELL CHECK", callback_data="spell_check")],
        [InlineKeyboardButton("🗑️ AUTO DELETE", callback_data="auto_delete"),
         InlineKeyboardButton("📚 RESULT MODE", callback_data="result_mode")],
        [InlineKeyboardButton("🗂 FILES MODE", callback_data="file_mode"),
         InlineKeyboardButton("📝 FILES CAPTION", callback_data="caption")],
        [InlineKeyboardButton("🥁 TUTORIAL LINK", callback_data="tutorial_link"),
         InlineKeyboardButton("🖇 SET SHORTLINK", callback_data="set_shortner")],
        [InlineKeyboardButton("‼️ CLOSE SETTINGS MENU ‼️", callback_data="close")]
    ]
    await message.reply(text, reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex("close"))
async def close_settings(client, query: CallbackQuery):
    await query.message.delete()

@Client.on_callback_query()
async def handle_callbacks(client, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in BOT_OWNER:
        return await query.answer("🚫 Not allowed", show_alert=True)

    data = query.data
    settings = user_settings.setdefault(user_id, {
        "force_channels": [],
        "max_results": 5,
        "imdb": False,
        "spell_check": True,
        "auto_delete": False,
        "delete_time": "20m",
        "result_mode": "link",
        "file_mode": {"type": "verify", "second_verify": False, "verify_time": "300", "log_channel": ""},
        "caption": None,
        "tutorial_links": {"first": "", "second": ""},
        "shortlinks": {"1": "", "2": ""},
        "awaiting_input": None
    })

    async def back_button():
        return InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data="back_main")]])

    if data == "back_main":
        return await settings_menu(client, query.message)

    if data == "force_channel":
        txt = "**ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪʙᴇ ᴄʜᴀɴɴᴇʟ IDꜱ.**"
        btn = [
            [InlineKeyboardButton("Set Channel", callback_data="set_force"),
             InlineKeyboardButton("Delete Channel", callback_data="del_force")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data == "set_force":
        settings["awaiting_input"] = {"type": "force"}
        return await query.message.edit("Send me Channel IDs (space separated)\n/cancel - Cancel this process.", reply_markup=await back_button())

    if data == "del_force":
        settings["force_channels"] = []
        return await query.message.edit("✅ Channels deleted.", reply_markup=await back_button())

    if data == "max_results":
        settings["awaiting_input"] = {"type": "max"}
        return await query.message.edit("Send max results (number)\n/cancel - Cancel this process.", reply_markup=await back_button())

    if data == "imdb":
        imdb = settings["imdb"]
        settings["imdb"] = not imdb
        status = "ON ✅" if not imdb else "OFF ❌"
        txt = f"""**ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ɪᴍᴅʙ sᴇᴛᴛɪɴɢ.ɪᴍᴅʙ ᴘᴏꜱᴛᴇʀ - {status}**
**ɪᴍᴅʙ ᴛᴇᴍᴘʟᴀᴛᴇ - 🏷 ᴛɪᴛʟᴇ -** {{title}} **📢 ʀᴇǫᴜᴇꜱᴛᴇᴅ ʙʏ - {{mention}} ♾️ ᴘᴏᴡᴇʀᴇᴅ ʙʏ - {{group}}**"""
        btn = [[InlineKeyboardButton("On Poster", callback_data="imdb")], [InlineKeyboardButton("<< BACK", callback_data="back_main")]]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data == "spell_check":
        spell = settings["spell_check"]
        settings["spell_check"] = not spell
        txt = f"""**ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʙᴏᴛ ꜱᴘᴇʟʟɪɴɢ ᴄʜᴇᴄᴋ ᴍᴇꜱꜱᴀɢᴇꜱ**
**ꜱᴘᴇʟʟ ᴄʜᴇᴄᴋ - {'ON ✅' if not spell else 'OFF ❌'}**"""
        btn = [[InlineKeyboardButton("Turn off" if not spell else "Turn on", callback_data="spell_check")], [InlineKeyboardButton("<< BACK", callback_data="back_main")]]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data == "auto_delete":
        ad = settings["auto_delete"]
        settings["auto_delete"] = not ad
        txt = f"""**ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ɢɪᴠᴇɴ ꜰɪʟᴇꜱ ᴅᴇʟᴇᴛᴇ ꜱᴇᴛᴛɪɴɢ**
**ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ - {'ON ✅' if not ad else 'OFF ❌'}**
**ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇ - {settings['delete_time']}**"""
        btn = [
            [InlineKeyboardButton("Set Time", callback_data="set_delete_time")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data == "set_delete_time":
        settings["awaiting_input"] = {"type": "delete_time"}
        return await query.message.edit("Send time like `1h` or `15m`\n/cancel - Cancel this process.", reply_markup=await back_button())

    if data == "result_mode":
        rm = settings["result_mode"]
        new = "button" if rm == "link" else "link"
        settings["result_mode"] = new
        txt = f"""**ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ɢɪᴠᴇɴ ʀᴇꜱᴜʟᴛ ᴍᴏᴅᴇ.
ʀᴇꜱᴜʟᴛ ᴍᴏᴅᴇ - {'🖇 LINKS' if new == 'link' else '🎯 BUTTON'}**"""
        btn = [[InlineKeyboardButton("Set button mode", callback_data="result_mode")], [InlineKeyboardButton("<< BACK", callback_data="back_main")]]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data == "caption":
        settings["awaiting_input"] = {"type": "caption"}
        return await query.message.edit("Send me new file caption.\n/cancel - Cancel this process.", reply_markup=await back_button())

    if data == "file_mode":
        settings["file_mode"]["type"] = "shortlink" if settings["file_mode"]["type"] == "verify" else "verify"
        txt = f"""**ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ꜰɪʟᴇꜱ ᴍᴏᴅᴇ.
ꜰɪʟᴇ ᴍᴏᴅᴇ - {'♻️ VERIFY' if settings['file_mode']['type'] == 'verify' else '📎 SHORTLINK'}**"""
        btn = [
            [InlineKeyboardButton("Set shortner mode", callback_data="file_mode")],
            [InlineKeyboardButton("Is second verify", callback_data="second_verify")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data == "second_verify":
        settings["file_mode"]["second_verify"] = not settings["file_mode"]["second_verify"]
        return await handle_callbacks(client, query)

    if data == "tutorial_link":
        links = settings["tutorial_links"]
        txt = f"""**⚠️ ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ʙᴏᴛ ᴛᴜᴛᴏʀɪᴀʟ ᴠɪᴅᴇᴏ ʟɪɴᴋ.ꜰɪʀꜱᴛ -**
{links['first'] or '❌ Not Set'}
**ꜱᴇᴄᴏɴᴅ -**
{links['second'] or '❌ Not Set'}"""
        btn = [
            [InlineKeyboardButton("Set First", callback_data="set_tutorial_first"),
             InlineKeyboardButton("Set Second", callback_data="set_tutorial_second")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data in ["set_tutorial_first", "set_tutorial_second"]:
        which = "first" if "first" in data else "second"
        settings["awaiting_input"] = {"type": "tutorial", "which": which}
        return await query.message.edit("Send me the tutorial link.\n/cancel - Cancel this process.", reply_markup=await back_button())

    if data == "set_shortner":
        sl = settings["shortlinks"]
        txt = f"""**ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ꜱʜᴏʀᴛʟɪɴᴋꜱ
1ꜱᴛ -** {sl['1'] or '❌ Not Set'}
**2ɴᴅ -** {sl['2'] or '❌ Not Set'}"""
        btn = [
            [InlineKeyboardButton("Set First", callback_data="set_short_1"),
             InlineKeyboardButton("Set Second", callback_data="set_short_2")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data.startswith("set_short_"):
        which = "1" if "1" in data else "2"
        settings["awaiting_input"] = {"type": "shortlink", "which": which}
        return await query.message.edit("Send your shortlink url.\n/cancel - Cancel this process.", reply_markup=await back_button())

@Client.on_message(filters.private & filters.text)
async def handle_text(client, message: Message):
    user_id = message.from_user.id
    if user_id not in BOT_OWNER:
        return

    settings = user_settings.setdefault(user_id, {})
    state = settings.get("awaiting_input")
    if not state:
        return

    text = message.text.strip()

    if text.lower() == "/cancel":
        settings["awaiting_input"] = None
        return await message.reply("❌ CANCELLED THIS PROCESS", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data="back_main")]]))

    typ = state["type"]
    if typ == "force":
        settings["force_channels"] = text.split()
        await message.reply("✅ CHANNELS SAVED")
    elif typ == "max":
        if text.isdigit():
            settings["max_results"] = int(text)
            await message.reply("✅ MAX RESULTS SAVED")
    elif typ == "delete_time":
        settings["delete_time"] = text
        await message.reply("✅ DELETE TIME SAVED")
    elif typ == "caption":
        settings["caption"] = text
        await message.reply("✅ CAPTION SAVED")
    elif typ == "tutorial":
        settings["tutorial_links"][state["which"]] = text
        await message.reply("✅ TUTORIAL LINK SAVED")
    elif typ == "shortlink":
        settings["shortlinks"][state["which"]] = text
        await message.reply("✅ SHORTLINK SAVED")

    settings["awaiting_input"] = None
