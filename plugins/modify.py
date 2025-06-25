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
        [InlineKeyboardButton("🈵 IMDB", callback_data="imdb_toggle"),
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

@Client.on_callback_query()
async def handle_settings_buttons(client, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in BOT_OWNER:
        return await query.answer("🚫 Not allowed.", show_alert=True)

    data = query.data
    settings = user_settings.setdefault(user_id, {
        "force_channels": [],
        "auto_delete": False,
        "imdb": True,
        "spell_check": True,
        "result_mode": "link",
        "file_mode": {"type": "verify", "second_verify": True},
        "shortlink": {},
        "tutorial_links": {},
        "caption": None,
        "max_results": 5,
        "awaiting_input": None,
        "delete_time": "20m"
    })

    def back_btn():
        return [[InlineKeyboardButton("<< BACK", callback_data="back_main")]]

    if data == "force_channel":
        txt = "**ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪʙᴇ ᴄʜᴀɴɴᴇʟ IDꜱ.**\n\n"
        txt += f"**ꜰᴏʀᴄᴇ ᴄʜᴀɴɴᴇʟꜱ -** {', '.join(settings['force_channels']) or '❌ NONE'}"
        btn = [
            [InlineKeyboardButton("SET CHANNEL", callback_data="set_force_channel"),
             InlineKeyboardButton("DELETE CHANNEL", callback_data="del_force_channel")],
            *back_btn()
        ]
        await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    elif data == "set_force_channel":
        settings["awaiting_input"] = {"type": "force_channel"}
        await query.message.edit("**ꜱᴇɴᴅ ᴍᴇ ᴄʜᴀɴɴᴇʟ ID(S) ᴡɪᴛʜ ꜱᴘᴀᴄᴇ.**\n/cancel - ᴄᴀɴᴄᴇʟ ᴛʜɪꜱ ᴘʀᴏᴄᴇss.")

    elif data == "del_force_channel":
        settings["force_channels"] = []
        await query.message.edit("✅ CHANNELS DELETED.", reply_markup=InlineKeyboardMarkup(back_btn()))

    elif data == "max_results":
        settings["awaiting_input"] = {"type": "max_results"}
        await query.message.edit("**ꜱᴇɴᴅ ᴍᴀx ʀᴇꜱᴜʟᴛꜱ (ɴᴜᴍʙᴇʀ).**\n/cancel - ᴄᴀɴᴄᴇʟ ᴛʜɪꜱ ᴘʀᴏᴄᴇss.")

    elif data == "imdb_toggle":
        settings["imdb"] = not settings["imdb"]
        status = "✅ ON" if settings["imdb"] else "❌ OFF"
        await query.message.edit(f"**IMDB POSTER - {status}**", reply_markup=InlineKeyboardMarkup(back_btn()))

    elif data == "spell_toggle":
        settings["spell_check"] = not settings["spell_check"]
        status = "✅" if settings["spell_check"] else "❌"
        await query.message.edit(f"**SPELL CHECK - {status}**", reply_markup=InlineKeyboardMarkup(back_btn()))

    elif data == "auto_delete":
        settings["auto_delete"] = not settings["auto_delete"]
        status = "✅ ON" if settings["auto_delete"] else "❌ OFF"
        txt = f"**AUTO DELETE - {status}**\nDELETE TIME - {settings['delete_time']}"
        btn = [
            [InlineKeyboardButton("SET TIME", callback_data="set_delete_time")],
            *back_btn()
        ]
        await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    elif data == "set_delete_time":
        settings["awaiting_input"] = {"type": "auto_delete_time"}
        await query.message.edit("**SEND TIME LIKE - `1h` or `15m`.**\n/cancel - CANCEL THIS PROCESS.")

    elif data == "result_mode":
        rm = "button" if settings["result_mode"] == "link" else "link"
        settings["result_mode"] = rm
        await query.message.edit(f"**RESULT MODE - {'BUTTON' if rm == 'button' else 'LINK'}**", reply_markup=InlineKeyboardMarkup(back_btn()))

    elif data == "file_mode":
        fmode = settings["file_mode"]
        fmode["type"] = "shortlink" if fmode["type"] == "verify" else "verify"
        await query.message.edit(f"**FILES MODE: {fmode['type'].upper()}**", reply_markup=InlineKeyboardMarkup(back_btn()))

    elif data == "caption":
        settings["awaiting_input"] = {"type": "caption"}
        await query.message.edit("SEND ME NEW FILE CAPTION.\n/cancel - CANCEL THIS PROCESS.")

    elif data == "set_shortner":
        sl = settings["shortlink"]
        txt = f"""**ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ꜱʜᴏʀᴛʟɪɴᴋꜱ.**

[ᴅᴇꜰᴀᴜʟᴛ] 1ꜱᴛ - easysky.in **** {sl.get('1', '❌')}
[ᴅᴇꜰᴀᴜʟᴛ] 2ɴᴅ - linkmonetizer.in **** {sl.get('2', '❌')}"""
        btn = [
            [InlineKeyboardButton("1ST SHORTNER", callback_data="shortner_1"),
             InlineKeyboardButton("2ND SHORTNER", callback_data="shortner_2")],
            [InlineKeyboardButton("DELETE SHORTNER", callback_data="del_shortner")],
            *back_btn()
        ]
        await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    elif data == "del_shortner":
        sl = settings["shortlink"]
        txt = f"""**ᴡʜɪᴄʜ ꜱʜᴏʀᴛɴᴇʀ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ??
1ꜱᴛ ꜱʜᴏʀᴛʟɪɴᴋ -** easysky.in **** {sl.get('1', '❌')}  
**2ɴᴅ ꜱʜᴏʀᴛʟɪɴᴋ -** linkmonetizer.in **** {sl.get('2', '❌')}"""
        btn = [
            [InlineKeyboardButton("FIRST", callback_data="del_s1"),
             InlineKeyboardButton("SECOND", callback_data="del_s2"),
             InlineKeyboardButton("BOTH", callback_data="del_sb")],
            *back_btn()
        ]
        await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    elif data == "del_s1":
        settings["shortlink"].pop("1", None)
        await handle_settings_buttons(client, query)
    elif data == "del_s2":
        settings["shortlink"].pop("2", None)
        await handle_settings_buttons(client, query)
    elif data == "del_sb":
        settings["shortlink"] = {}
        await handle_settings_buttons(client, query)

    elif data == "shortner_1" or data == "shortner_2":
        settings["awaiting_input"] = {"type": "shortner", "which": data[-1]}
        await query.message.edit("SEND SHORTLINK URL (without https://)\n/cancel - CANCEL THIS PROCESS.")

    elif data == "tutorial_link":
        tl = settings["tutorial_links"]
        txt = f"""**⚠️ ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ʙᴏᴛ ᴛᴜᴛᴏʀɪᴀʟ ᴠɪᴅᴇᴏ ʟɪɴᴋꜱ.**
ꜰɪʀꜱᴛ - https://t.me/HOW_TO_USE_BISHNOI_BOTZ/36  
ꜱᴇᴄᴏɴᴅ - https://t.me/HOW_TO_USE_BISHNOI_BOTZ/34"""
        btn = [
            [InlineKeyboardButton("1ST TUTORIAL", callback_data="tutorial_1"),
             InlineKeyboardButton("2ND TUTORIAL", callback_data="tutorial_2")],
            [InlineKeyboardButton("DELETE TUTORIAL", callback_data="del_tutorial")],
            *back_btn()
        ]
        await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    elif data == "del_tutorial":
        tl = settings["tutorial_links"]
        txt = f"""**⚠️ ᴡʜɪᴄʜ ᴛᴜᴛᴏʀɪᴀʟ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ?
ꜰɪʀꜱᴛ -** https://t.me/HOW_TO_USE_BISHNOI_BOTZ/36  
**ꜱᴇᴄᴏɴᴅ -** https://t.me/HOW_TO_USE_BISHNOI_BOTZ/34"""
        btn = [
            [InlineKeyboardButton("FIRST", callback_data="del_t1"),
             InlineKeyboardButton("SECOND", callback_data="del_t2"),
             InlineKeyboardButton("BOTH", callback_data="del_tb")],
            *back_btn()
        ]
        await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    elif data == "del_t1":
        settings["tutorial_links"].pop("first", None)
        await handle_settings_buttons(client, query)
    elif data == "del_t2":
        settings["tutorial_links"].pop("second", None)
        await handle_settings_buttons(client, query)
    elif data == "del_tb":
        settings["tutorial_links"] = {}
        await handle_settings_buttons(client, query)

    elif data.startswith("tutorial_"):
        which = "first" if data.endswith("1") else "second"
        settings["awaiting_input"] = {"type": "tutorial", "which": which}
        await query.message.edit("SEND ME A TUTORIAL LINK.\n/cancel - CANCEL THIS PROCESS.")

    elif data == "back_main":
        await settings_menu(client, query.message)

@Client.on_message(filters.private & filters.text)
async def handle_inputs(client, message: Message):
    user_id = message.from_user.id
    if user_id not in BOT_OWNER:
        return
    settings = user_settings.setdefault(user_id, {})
    state = settings.get("awaiting_input")
    text = message.text.strip()

    if text.lower() == "/cancel":
        settings["awaiting_input"] = None
        return await message.reply("❌ CANCELLED.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data="back_main")]]))

    if not state:
        return

    t = state["type"]
    if t == "force_channel":
        settings["force_channels"] = text.split()
        await message.reply("✅ FORCE CHANNELS SAVED.")
    elif t == "shortner":
        settings["shortlink"][state["which"]] = text
        await message.reply(f"✅ SHORTNER {state['which']} SAVED.")
    elif t == "tutorial":
        settings["tutorial_links"][state["which"]] = text
        await message.reply(f"✅ TUTORIAL {state['which']} LINK SAVED.")
    elif t == "caption":
        settings["caption"] = text
        await message.reply("✅ CAPTION SAVED.")
    elif t == "max_results":
        if not text.isdigit():
            return await message.reply("❌ INVALID. Please enter a number.")
        settings["max_results"] = int(text)
        await message.reply("✅ MAX RESULTS SAVED.")
    elif t == "auto_delete_time":
        settings["delete_time"] = text
        await message.reply("✅ DELETE TIME SAVED.")
    settings["awaiting_input"] = None
