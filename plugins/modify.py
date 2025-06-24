from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import BOT_OWNER  # Make sure your config file has BOT_OWNER = [123456789]

# Temporary in-memory settings per user
user_settings = {}

@Client.on_message(filters.command("modify") & filters.private)
async def modify_private(client, message: Message):
    if message.from_user.id not in BOT_OWNER:
        return await message.reply("You are not authorized to use this command.")
    await settings_menu(client, message)

@Client.on_message(filters.command("modify") & filters.group)
async def modify_group(client, message: Message):
    if message.from_user.id not in BOT_OWNER:
        return
    btn = [[InlineKeyboardButton("🤖 Open Settings in PM", url=f"https://t.me/{client.me.username}?start=modify")]]
    await message.reply("⚙️ Please use this command in private chat.", reply_markup=InlineKeyboardMarkup(btn))


async def settings_menu(client, message):
    text = "**⚙️ CUSTOMIZE YOUR SETTINGS AS PER YOUR GROUP NEEDS ✨**"
    btn = [
        [InlineKeyboardButton("👥 FORCE CHANNEL", callback_data="force_channel")],
        [InlineKeyboardButton("ℹ️ MAX RESULTS", callback_data="max_results"),
         InlineKeyboardButton("🗑️ AUTO DELETE", callback_data="auto_delete")],
        [InlineKeyboardButton("🈵 IMDB", callback_data="imdb_toggle"),
         InlineKeyboardButton("🔎 SPELL CHECK", callback_data="spell_toggle")],
        [InlineKeyboardButton("📚 RESULT MODE", callback_data="result_mode"),
         InlineKeyboardButton("📦 FILE MODE", callback_data="file_mode")],
        [InlineKeyboardButton("📝 CAPTION", callback_data="caption"),
         InlineKeyboardButton("🪝 SET SHORTNER", callback_data="set_shortner")],
        [InlineKeyboardButton("🥁 TUTORIAL LINK", callback_data="tutorial_link")],
        [InlineKeyboardButton("‼️ CLOSE SETTINGS MENU ‼️", callback_data="close")]
    ]
    await message.reply(text, reply_markup=InlineKeyboardMarkup(btn))


@Client.on_callback_query(filters.regex("close"))
async def close_settings(client, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query()
async def handle_settings_buttons(client, query: CallbackQuery):
    user_id = query.from_user.id
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
        text = f"""**MANAGE FORCE SUBSCRIBE CHANNEL ID(S)**

**FORCE CHANNELS -** {', '.join(channels) if channels else 'None'}"""
        btn = [
            [InlineKeyboardButton("SET CHANNELS", callback_data="set_force_channel"),
             InlineKeyboardButton("DELETE CHANNEL", callback_data="del_force_channel")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        await query.message.edit(text, reply_markup=InlineKeyboardMarkup(btn))

    elif data == "set_force_channel":
        settings["awaiting_input"] = {"type": "force_channel"}
        await query.message.edit("SEND CHANNEL ID(S) WITH SPACE. /cancel TO CANCEL.")

    elif data == "del_force_channel":
        settings["force_channels"] = []
        await query.message.edit("✅ CHANNELS DELETED.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data="back_main")]]))

    elif data == "max_results":
        settings["awaiting_input"] = {"type": "max_results"}
        await query.message.edit("SEND MAX RESULT COUNT (number). /cancel TO CANCEL.")

    elif data == "auto_delete":
        settings["auto_delete"] = not settings["auto_delete"]
        await query.answer("✅ AUTO DELETE TOGGLED")
        await settings_menu(client, query.message)

    elif data == "imdb_toggle":
        settings["imdb"] = not settings["imdb"]
        await query.answer("✅ IMDB TOGGLED")
        await settings_menu(client, query.message)

    elif data == "spell_toggle":
        settings["spell_check"] = not settings["spell_check"]
        await query.answer("✅ SPELL CHECK TOGGLED")
        await settings_menu(client, query.message)

    elif data == "result_mode":
        current = settings["result_mode"]
        new_mode = "button" if current == "link" else "link"
        settings["result_mode"] = new_mode
        await query.message.edit(
            f"RESULT MODE - {'🖇 LINKS' if new_mode == 'link' else '🎯 BUTTONS'}",
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
        text = f"""**MANAGE FILES MODE**

Current Mode: {'♻️ VERIFY' if new_mode == 'verify' else '📎 SHORTLINK'}"""
        btn = [
            [InlineKeyboardButton("SET VERIFY MODE" if new_mode == "shortlink" else "SET SHORTNER MODE", callback_data="file_mode")],
            [InlineKeyboardButton(f"2ND VERIFY {'✅' if second else '❌'}", callback_data="toggle_second_verify")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        await query.message.edit(text, reply_markup=InlineKeyboardMarkup(btn))

    elif data == "toggle_second_verify":
        settings["file_mode"]["second_verify"] = not settings["file_mode"]["second_verify"]
        await handle_settings_buttons(client, query)

    elif data == "caption":
        settings["awaiting_input"] = {"type": "caption"}
        await query.message.edit("SEND NEW FILE CAPTION. /cancel TO CANCEL.")

    elif data == "set_shortner":
        sl = settings["shortlink"]
        text = f"""**MANAGE YOUR SHORTLINKS**

1ST SHORTNER - {sl.get('1', 'Not Set')}  
2ND SHORTNER - {sl.get('2', 'Not Set')}"""
        btn = [
            [InlineKeyboardButton("1ST SHORTNER", callback_data="shortner_1"),
             InlineKeyboardButton("2ND SHORTNER", callback_data="shortner_2")],
            [InlineKeyboardButton("DELETE SHORTNER", callback_data="del_shortner")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        await query.message.edit(text, reply_markup=InlineKeyboardMarkup(btn))

    elif data.startswith("shortner_"):
        which = data.split("_")[1]
        settings["awaiting_input"] = {"type": "shortner", "which": which}
        await query.message.edit("SEND SHORTLINK URL WITHOUT `https`. /cancel TO CANCEL.")

    elif data == "del_shortner":
        settings["shortlink"] = {}
        await query.message.edit("✅ SHORTNERS DELETED.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data="back_main")]]))

    elif data == "tutorial_link":
        tl = settings["tutorial_links"]
        text = f"""**TUTORIAL LINKS**

1ST - {tl.get('first', 'Not Set')}  
2ND - {tl.get('second', 'Not Set')}"""
        btn = [
            [InlineKeyboardButton("1ST TUTORIAL", callback_data="tutorial_1"),
             InlineKeyboardButton("2ND TUTORIAL", callback_data="tutorial_2")],
            [InlineKeyboardButton("DELETE TUTORIAL", callback_data="del_tutorial")],
            [InlineKeyboardButton("<< BACK", callback_data="back_main")]
        ]
        await query.message.edit(text, reply_markup=InlineKeyboardMarkup(btn))

    elif data.startswith("tutorial_"):
        which = "first" if data.endswith("1") else "second"
        settings["awaiting_input"] = {"type": "tutorial", "which": which}
        await query.message.edit("SEND ME A TUTORIAL LINK. /cancel TO CANCEL.")

    elif data == "del_tutorial":
        settings["tutorial_links"] = {}
        await query.message.edit("✅ TUTORIAL LINKS DELETED.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<< BACK", callback_data="back_main")]]))

    elif data == "back_main":
        await settings_menu(client, query.message)


@Client.on_message(filters.private & filters.text)
async def handle_input(client, message: Message):
    user_id = message.from_user.id
    text = message.text.strip()
    settings = user_settings.setdefault(user_id, {})
    state = settings.get("awaiting_input")

    if text.lower() == "/cancel":
        settings["awaiting_input"] = None
        return await message.reply("❌ CANCELLED.")

    if not state:
        return

    if state["type"] == "force_channel":
        settings["force_channels"] = text.split()
        await message.reply("✅ FORCE CHANNELS SAVED.")
    elif state["type"] == "shortner":
        key = state["which"]
        settings["shortlink"][key] = text
        await message.reply(f"✅ SHORTNER {key} SAVED.")
    elif state["type"] == "tutorial":
        key = state["which"]
        settings["tutorial_links"][key] = text
        await message.reply(f"✅ TUTORIAL {key.upper()} LINK SAVED.")
    elif state["type"] == "caption":
        settings["caption"] = text
        await message.reply("✅ CAPTION SET.")
    elif state["type"] == "max_results":
        if not text.isdigit():
            return await message.reply("Please enter a valid number.")
        settings["max_results"] = int(text)
        await message.reply("✅ MAX RESULTS SAVED.")

    settings["awaiting_input"] = None
