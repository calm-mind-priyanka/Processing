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

@Client.on_callback_query(filters.regex("close"))
async def close_settings(client, query: CallbackQuery):
    await query.message.delete()

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
        "awaiting_input": None
    })

    if data == "force_channel":
        channels = settings["force_channels"]
        txt = "**ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪʙᴇ ᴄʜᴀɴɴᴇʟ IDꜱ.**\n\n"
        txt += f"**ꜰᴏʀᴄᴇ ᴄʜᴀɴɴᴇʟꜱ -** {', '.join(channels) if channels else '❌ NONE'}"
        btn = [
            [InlineKeyboardButton("SET CHANNEL", callback_data="set_force_channel"),
             InlineKeyboardButton("DELETE CHANNEL", callback_data="del_force_channel")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    elif data == "set_force_channel":
        settings["awaiting_input"] = {"type": "force_channel"}
        await query.message.edit("**ꜱᴇɴᴅ ᴍᴇ ᴄʜᴀɴɴᴇʟ ID(S) ᴡɪᴛʜ ꜱᴘᴀᴄᴇ.**\n**ᴀɴᴅ ᴍᴀᴋᴇ ꜱᴜʀᴇ @Jhonwickrobot ɪꜱ ᴀᴅᴍɪɴ ɪɴ ᴀʟʟ ᴄʜᴀɴɴᴇʟꜱ.**\n/cancel - ᴄᴀɴᴄᴇʟ ᴛʜɪꜱ ᴘʀᴏᴄᴇss.")

    elif data == "del_force_channel":
        settings["force_channels"] = []
        await query.message.edit("✅ CHANNELS DELETED.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data="back_main")]]))

    elif data == "max_results":
        settings["awaiting_input"] = {"type": "max_results"}
        await query.message.edit("**ꜱᴇɴᴅ ᴍᴀx ʀᴇꜱᴜʟᴛꜱ (ɴᴜᴍʙᴇʀ).**\n/cancel - ᴄᴀɴᴄᴇʟ ᴛʜɪꜱ ᴘʀᴏᴄᴇss.")

    elif data == "auto_delete":
        settings["auto_delete"] = not settings["auto_delete"]
        await query.message.edit(f"""**ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ɢɪᴠᴇɴ ꜰɪʟᴇꜱ ᴅᴇʟᴇᴛᴇ ꜱᴇᴛᴛɪɴɢ.**

ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ - {"✅ ON" if settings["auto_delete"] else "❌ OFF"}
ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇ - 20 ᴍɪɴᴜᴛᴇꜱ""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("SET TIME", callback_data="set_delete_time"),
                 InlineKeyboardButton("OFF DELETE", callback_data="auto_delete")],
                [InlineKeyboardButton("<< BACK", callback_data="back_main")]
            ])
        )

    elif data == "set_delete_time":
        settings["awaiting_input"] = {"type": "auto_delete_time"}
        await query.message.edit("**ꜱᴇɴᴅ ᴛɪᴍᴇ ʟɪᴋᴇ - `1h` ᴏʀ `15m`.**\n/cancel - ᴄᴀɴᴄᴇʟ ᴛʜɪꜱ ᴘʀᴏᴄᴇss.")

    elif data == "imdb_toggle":
        settings["imdb"] = not settings["imdb"]
        imdb_status = "✅ ON" if settings["imdb"] else "❌ OFF"
        await query.message.edit(f"""**ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ɪᴍᴅʙ ꜱᴇᴛᴛɪɴɢꜱ.**

IMDB POSTER - {imdb_status}
IMDB TEMPLATE - 🏷 {{"{title}"}} | ᴘᴏᴡᴇʀᴇᴅ ʙʏ {{"{group}"}}

""", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("SET TEMPLATE", callback_data="set_imdb_template"),
             InlineKeyboardButton("DEFAULT TEMPLATE", callback_data="default_imdb_template")],
            [InlineKeyboardButton("ON POSTER", callback_data="imdb_toggle")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]))

    elif data == "spell_toggle":
        settings["spell_check"] = not settings["spell_check"]
        status = "✅" if settings["spell_check"] else "❌"
        await query.message.edit(f"**SPELL CHECK -** {status}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("TURN OFF" if settings["spell_check"] else "TURN ON", callback_data="spell_toggle")],
                [InlineKeyboardButton("<< BACK", callback_data="back_main")]
            ])
        )

    elif data == "result_mode":
        new_mode = "button" if settings["result_mode"] == "link" else "link"
        settings["result_mode"] = new_mode
        await query.message.edit(f"**RESULT MODE - {'🎯 BUTTONS' if new_mode == 'button' else '🖇 LINKS'}**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("SET LINK MODE" if new_mode == "button" else "SET BUTTON MODE", callback_data="result_mode")],
                [InlineKeyboardButton("<< BACK", callback_data="back_main")]
            ])
        )

    elif data == "file_mode":
        mode = settings["file_mode"]["type"]
        second = settings["file_mode"]["second_verify"]
        new_mode = "shortlink" if mode == "verify" else "verify"
        settings["file_mode"] = {"type": new_mode, "second_verify": second}
        txt = f"**FILES MODE: {'♻️ VERIFY' if new_mode == 'verify' else '📎 SHORTLINK'}**"
        btn = [
            [InlineKeyboardButton("TOGGLE MODE", callback_data="file_mode")],
            [InlineKeyboardButton(f"2ND VERIFY {'✅' if second else '❌'}", callback_data="toggle_second_verify")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    elif data == "toggle_second_verify":
        settings["file_mode"]["second_verify"] = not settings["file_mode"]["second_verify"]
        await handle_settings_buttons(client, query)

    elif data == "caption":
        settings["awaiting_input"] = {"type": "caption"}
        await query.message.edit("SEND ME NEW FILE CAPTION.\n/cancel - CANCEL THIS PROCESS.")

    elif data == "set_shortner":
        sl = settings["shortlink"]
        txt = f"""**SHORTLINK SETTINGS**

1ST SHORTLINK - {sl.get('1', '❌ NOT SET')}
2ND SHORTLINK - {sl.get('2', '❌ NOT SET')}"""
        btn = [
            [InlineKeyboardButton("1ST SHORTNER", callback_data="shortner_1"),
             InlineKeyboardButton("2ND SHORTNER", callback_data="shortner_2")],
            [InlineKeyboardButton("DELETE SHORTNER", callback_data="del_shortner")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    elif data.startswith("shortner_"):
        which = data.split("_")[1]
        settings["awaiting_input"] = {"type": "shortner", "which": which}
        await query.message.edit("SEND SHORTLINK URL WITHOUT https://\n/cancel - CANCEL THIS PROCESS.")

    elif data == "del_shortner":
        settings["shortlink"] = {}
        await query.message.edit("✅ SHORTNERS DELETED.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data="back_main")]]))

    elif data == "tutorial_link":
        tl = settings["tutorial_links"]
        txt = f"""**TUTORIAL LINKS**

1ST - {tl.get('first', '❌ NOT SET')}
2ND - {tl.get('second', '❌ NOT SET')}"""
        btn = [
            [InlineKeyboardButton("1ST TUTORIAL", callback_data="tutorial_1"),
             InlineKeyboardButton("2ND TUTORIAL", callback_data="tutorial_2")],
            [InlineKeyboardButton("DELETE TUTORIAL", callback_data="del_tutorial")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    elif data.startswith("tutorial_"):
        which = "first" if data.endswith("1") else "second"
        settings["awaiting_input"] = {"type": "tutorial", "which": which}
        await query.message.edit("SEND ME A TUTORIAL LINK.\n/cancel - CANCEL THIS PROCESS.")

    elif data == "del_tutorial":
        settings["tutorial_links"] = {}
        await query.message.edit("✅ TUTORIAL LINKS DELETED.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data="back_main")]]))

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
        return await message.reply("❌ CANCELLED.\n<< BACK", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data="back_main")]]))

    if not state:
        return

    if state["type"] == "force_channel":
        settings["force_channels"] = text.split()
        await message.reply("✅ FORCE CHANNELS SAVED.")
    elif state["type"] == "shortner":
        settings["shortlink"][state["which"]] = text
        await message.reply(f"✅ SHORTNER {state['which']} SAVED.")
    elif state["type"] == "tutorial":
        settings["tutorial_links"][state["which"]] = text
        await message.reply(f"✅ TUTORIAL {state['which']} LINK SAVED.")
    elif state["type"] == "caption":
        settings["caption"] = text
        await message.reply("✅ CAPTION SAVED.")
    elif state["type"] == "max_results":
        if not text.isdigit():
            return await message.reply("❌ INVALID. Please enter a number.")
        settings["max_results"] = int(text)
        await message.reply("✅ MAX RESULTS SAVED.")
    elif state["type"] == "auto_delete_time":
        settings["delete_time"] = text
        await message.reply("✅ DELETE TIME SAVED.")
    settings["awaiting_input"] = None
