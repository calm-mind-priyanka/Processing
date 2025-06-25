# modify.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

BOT_OWNER = [6046055058]
user_settings = {}

@Client.on_message(filters.private & filters.command("modify"))
async def modify_command(client, message: Message):
    if message.from_user.id not in BOT_OWNER:
        return await message.reply("🚫 You are not authorized.")
    await settings_menu(client, message)

async def settings_menu(client, message_or_query, group_title="YOUR GROUP", group_id="PRIVATE"):
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
         InlineKeyboardButton("📝 FILE CAPTION", callback_data="caption")],
        [InlineKeyboardButton("🥁 TUTORIAL LINK", callback_data="tutorial_link"),
         InlineKeyboardButton("🖇 SET SHORTLINK", callback_data="set_shortlink")],
        [InlineKeyboardButton("✅ FILE SECURE", callback_data="file_secure")],
        [InlineKeyboardButton("‼️ CLOSE SETTINGS MENU ‼️", callback_data="close")]
    ]
    if isinstance(message_or_query, Message):
        await message_or_query.reply(text, reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message_or_query.message.edit(text, reply_markup=InlineKeyboardMarkup(btn))

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
        "file_secure": False,
        "awaiting_input": None
    })

    def back_btn(to="back_main"):
        return InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data=to)]])

    if data == "back_main":
        return await settings_menu(client, query)

    if data == "close":
        return await query.message.delete()

    if data == "force_channel":
        txt = "**Manage force subscribe channels.**"
        btn = [
            [InlineKeyboardButton("Set Channel", callback_data="set_force"),
             InlineKeyboardButton("Delete Channel", callback_data="del_force")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data == "set_force":
        settings["awaiting_input"] = {"type": "force"}
        return await query.message.edit("Send Channel IDs separated by space.\n/cancel", reply_markup=back_btn())

    if data == "del_force":
        settings["force_channels"] = []
        return await query.message.edit("✅ Channels deleted.", reply_markup=back_btn())

    if data == "max_results":
        settings["awaiting_input"] = {"type": "max"}
        return await query.message.edit("Send max results number.\n/cancel", reply_markup=back_btn())

    if data == "imdb":
        settings["imdb"] = not settings["imdb"]
        txt = f"""**IMDB SETTINGS**
**Poster - {'ON ✅' if settings['imdb'] else 'OFF ❌'}**
**Template - 🏷 TITLE -** {{title}} **📢 REQUESTED BY - {{mention}} ♾️ POWERED BY - {{group}}**"""
        btn = [[InlineKeyboardButton("On Poster", callback_data="imdb")], [InlineKeyboardButton("<< BACK", callback_data="back_main")]]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data == "spell_check":
        settings["spell_check"] = not settings["spell_check"]
        txt = f"""**SPELLING CHECK SETTINGS**
**Spell Check - {'ON ✅' if settings['spell_check'] else 'OFF ❌'}**"""
        btn = [[InlineKeyboardButton("Turn off" if settings["spell_check"] else "Turn on", callback_data="spell_check")], [InlineKeyboardButton("<< BACK", callback_data="back_main")]]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data == "auto_delete":
        txt = f"""**AUTO DELETE SETTINGS**
**Auto Delete - {'ON ✅' if not settings['auto_delete'] else 'OFF ❌'}**
**Delete Time - {settings['delete_time']}**"""
        settings["auto_delete"] = not settings["auto_delete"]
        btn = [
            [InlineKeyboardButton("Set Time", callback_data="set_delete_time")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data == "set_delete_time":
        settings["awaiting_input"] = {"type": "delete_time"}
        return await query.message.edit("Send time like `15m` or `2h`\n/cancel", reply_markup=back_btn())

    if data == "result_mode":
        settings["result_mode"] = "button" if settings["result_mode"] == "link" else "link"
        txt = f"""**RESULT MODE SETTINGS**
**Result Mode - {'🖇 LINKS' if settings['result_mode'] == 'link' else '🎯 BUTTON'}**"""
        btn = [[InlineKeyboardButton("Set button mode", callback_data="result_mode")], [InlineKeyboardButton("<< BACK", callback_data="back_main")]]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data == "caption":
        settings["awaiting_input"] = {"type": "caption"}
        return await query.message.edit("Send file caption.\n/cancel", reply_markup=back_btn())

    if data == "file_mode":
        mode = settings["file_mode"]["type"]
        settings["file_mode"]["type"] = "shortlink" if mode == "verify" else "verify"
        txt = f"""**FILE MODE SETTINGS**
**File Mode - {'♻️ VERIFY' if settings['file_mode']['type']=='verify' else '📎 SHORTLINK'}**"""
        btn = [
            [InlineKeyboardButton("Set shortner mode", callback_data="file_mode")],
            [InlineKeyboardButton("Is second verify", callback_data="second_verify")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data == "second_verify":
        settings["file_mode"]["second_verify"] = not settings["file_mode"]["second_verify"]
        txt = f"""**2ND VERIFY SETTINGS**
**2nd Verification - {'ON ✅' if settings['file_mode']['second_verify'] else 'OFF ❌'}**
**Time - {settings['file_mode']['verify_time']}**
**Log Channel - {settings['file_mode']['log_channel'] or '❌ Not Set'}**"""
        btn = [
            [InlineKeyboardButton("Set Time", callback_data="set_second_time"),
             InlineKeyboardButton("Set Log Channel", callback_data="set_log_channel")],
            [InlineKeyboardButton("<< BACK", callback_data="file_mode")]
        ]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data == "set_second_time":
        settings["awaiting_input"] = {"type": "verify_time"}
        return await query.message.edit("Send time in seconds (e.g. 300)\n/cancel", reply_markup=back_btn("file_mode"))

    if data == "set_log_channel":
        settings["awaiting_input"] = {"type": "log_channel"}
        return await query.message.edit("Send log channel ID.\n/cancel", reply_markup=back_btn("file_mode"))

    if data == "tutorial_link":
        links = settings["tutorial_links"]
        txt = f"""**TUTORIAL VIDEO LINKS**
**First -** {links['first'] or '❌ Not Set'}
**Second -** {links['second'] or '❌ Not Set'}"""
        btn = [
            [InlineKeyboardButton("Set First", callback_data="set_tut_1"),
             InlineKeyboardButton("Set Second", callback_data="set_tut_2")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data.startswith("set_tut_"):
        which = "first" if "1" in data else "second"
        settings["awaiting_input"] = {"type": "tutorial", "which": which}
        return await query.message.edit("Send tutorial video link.\n/cancel", reply_markup=back_btn())

    if data == "set_shortlink":
        sl = settings["shortlinks"]
        txt = f"""**SET SHORTLINK**
**1st -** {sl['1'] or '❌ Not Set'}
**2nd -** {sl['2'] or '❌ Not Set'}"""
        btn = [
            [InlineKeyboardButton("Set First", callback_data="set_short_1"),
             InlineKeyboardButton("Set Second", callback_data="set_short_2")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    if data.startswith("set_short_"):
        which = "1" if "1" in data else "2"
        settings["awaiting_input"] = {"type": "shortlink", "which": which}
        return await query.message.edit("Send shortlink URL.\n/cancel", reply_markup=back_btn())

    if data == "file_secure":
        settings["file_secure"] = not settings["file_secure"]
        txt = f"""**FILE SECURE - {'ON ✅' if settings['file_secure'] else 'OFF ❌'}**"""
        btn = [[InlineKeyboardButton("Toggle", callback_data="file_secure")], [InlineKeyboardButton("<< BACK", callback_data="back_main")]]
        return await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

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
    elif typ == "verify_time":
        settings["file_mode"]["verify_time"] = text
        await message.reply("✅ VERIFY TIME SAVED")
    elif typ == "log_channel":
        settings["file_mode"]["log_channel"] = text
        await message.reply("✅ LOG CHANNEL SAVED")
    settings["awaiting_input"] = None
