from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Only you (admin) can access /modify
BOT_OWNER = [6046055058]
user_settings = {}

# /modify in PM only
@Client.on_message(filters.private & filters.command("modify"))
async def modify_command(client, message: Message):
    if message.from_user.id not in BOT_OWNER:
        return await message.reply("🚫 You are not authorized.")
    await settings_menu(client, message)

# Settings menu layout
async def settings_menu(client, message, group_title="Your Group", group_id="PRIVATE"):
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

# Close settings menu
@Client.on_callback_query(filters.regex("close"))
async def close_settings(client, query: CallbackQuery):
    await query.message.delete()

# Handle button logic
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
        txt = f"**FORCE CHANNELS:** {', '.join(channels) if channels else 'None'}"
        btn = [
            [InlineKeyboardButton("SET CHANNELS", callback_data="set_force_channel"),
             InlineKeyboardButton("DELETE CHANNEL", callback_data="del_force_channel")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    elif data == "set_force_channel":
        settings["awaiting_input"] = {"type": "force_channel"}
        await query.message.edit("SEND CHANNEL ID(S) (space separated). /cancel to stop.")

    elif data == "del_force_channel":
        settings["force_channels"] = []
        await query.message.edit("✅ CHANNELS DELETED.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data="back_main")]]))

    elif data == "max_results":
        settings["awaiting_input"] = {"type": "max_results"}
        await query.message.edit("SEND MAX RESULTS NUMBER. /cancel to stop.")

    elif data == "auto_delete":
        settings["auto_delete"] = not settings["auto_delete"]
        await query.answer("✅ TOGGLED AUTO DELETE")
        await settings_menu(client, query.message)

    elif data == "imdb_toggle":
        settings["imdb"] = not settings["imdb"]
        await query.answer("✅ TOGGLED IMDB")
        await settings_menu(client, query.message)

    elif data == "spell_toggle":
        settings["spell_check"] = not settings["spell_check"]
        await query.answer("✅ TOGGLED SPELL CHECK")
        await settings_menu(client, query.message)

    elif data == "result_mode":
        new_mode = "button" if settings["result_mode"] == "link" else "link"
        settings["result_mode"] = new_mode
        await query.message.edit(
            f"RESULT MODE - {'🖇 LINKS' if new_mode == 'link' else '🎯 BUTTONS'}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("TOGGLE AGAIN", callback_data="result_mode")],
                [InlineKeyboardButton("<< BACK", callback_data="back_main")]
            ])
        )

    elif data == "file_mode":
        mode = settings["file_mode"]["type"]
        second = settings["file_mode"]["second_verify"]
        new_mode = "shortlink" if mode == "verify" else "verify"
        settings["file_mode"] = {"type": new_mode, "second_verify": second}
        txt = f"MODE: {'♻️ VERIFY' if new_mode == 'verify' else '📎 SHORTLINK'}"
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
        await query.message.edit("SEND NEW CAPTION. /cancel to stop.")

    elif data == "set_shortner":
        sl = settings["shortlink"]
        txt = f"""SHORTLINKS:
1 - {sl.get('1', '❌ Not Set')}
2 - {sl.get('2', '❌ Not Set')}"""
        btn = [
            [InlineKeyboardButton("SET 1", callback_data="shortner_1"),
             InlineKeyboardButton("SET 2", callback_data="shortner_2")],
            [InlineKeyboardButton("DELETE ALL", callback_data="del_shortner")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    elif data.startswith("shortner_"):
        which = data.split("_")[1]
        settings["awaiting_input"] = {"type": "shortner", "which": which}
        await query.message.edit("SEND SHORTLINK (without https). /cancel to stop.")

    elif data == "del_shortner":
        settings["shortlink"] = {}
        await query.message.edit("✅ SHORTNERS CLEARED.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data="back_main")]]))

    elif data == "tutorial_link":
        tl = settings["tutorial_links"]
        txt = f"""TUTORIAL LINKS:
1 - {tl.get('first', '❌ Not Set')}
2 - {tl.get('second', '❌ Not Set')}"""
        btn = [
            [InlineKeyboardButton("SET 1", callback_data="tutorial_1"),
             InlineKeyboardButton("SET 2", callback_data="tutorial_2")],
            [InlineKeyboardButton("DELETE ALL", callback_data="del_tutorial")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        await query.message.edit(txt, reply_markup=InlineKeyboardMarkup(btn))

    elif data.startswith("tutorial_"):
        which = "first" if data.endswith("1") else "second"
        settings["awaiting_input"] = {"type": "tutorial", "which": which}
        await query.message.edit("SEND TUTORIAL LINK. /cancel to stop.")

    elif data == "del_tutorial":
        settings["tutorial_links"] = {}
        await query.message.edit("✅ TUTORIAL LINKS CLEARED.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data="back_main")]]))

    elif data == "back_main":
        await settings_menu(client, query.message)

# Handle text input after button triggers
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
        return await message.reply("❌ CANCELLED.")

    if not state:
        return

    if state["type"] == "force_channel":
        settings["force_channels"] = text.split()
        await message.reply("✅ CHANNELS SET.")
    elif state["type"] == "shortner":
        settings["shortlink"][state["which"]] = text
        await message.reply(f"✅ SHORTNER {state['which']} SET.")
    elif state["type"] == "tutorial":
        settings["tutorial_links"][state["which"]] = text
        await message.reply(f"✅ TUTORIAL {state['which']} SET.")
    elif state["type"] == "caption":
        settings["caption"] = text
        await message.reply("✅ CAPTION SET.")
    elif state["type"] == "max_results":
        if not text.isdigit():
            return await message.reply("❌ INVALID. Please send a number.")
        settings["max_results"] = int(text)
        await message.reply("✅ MAX RESULTS SET.")
    settings["awaiting_input"] = None
