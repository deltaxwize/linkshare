from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from datetime import datetime
import time
import asyncio
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, ADMINS, START_PIC, LINK_PIC
from utils import encode_channel_id, decode_channel_id
from datetime import datetime, timedelta
from pyrogram.enums import ChatType
from aiohttp import web
import threading
import os

app = Client("invite_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URI)
db = mongo['invite_bot']
users_col = db['users']
channels_col = db['channels']

@app.on_message(filters.command("start"))
async def start_handler(_, message: Message):
    users_col.update_one({"_id": message.from_user.id}, {"$set": {"name": message.from_user.first_name}}, upsert=True)
    args = message.text.split(" ", 1)
    start_text = ("<b><blockquote>𝖡𝖺𝗄𝗄𝖺 𝖨’𝗆 𝗍𝗁𝖾 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖫𝗂𝗇𝗄 𝖡𝗈𝗍 — 𝖨 𝖼𝗋𝖾𝖺𝗍𝖾 𝗌𝗆𝖺𝗋𝗍 𝗋𝖾𝖽𝗂𝗋𝖾𝖼𝗍 𝗅𝗂𝗇𝗄𝗌 𝖿𝗈𝗋 𝗒𝗈𝗎𝗋 𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝖼𝗁𝖺𝗇𝗇𝖾𝗅𝗌 𝗍𝗈 𝗁𝖾𝗅𝗉 𝖺𝗏𝗈𝗂𝖽 𝗉𝗋𝗈𝖻𝗅𝖾𝗆𝗌 𝖺𝗇𝖽 𝗄𝖾𝖾𝗉 𝗍𝗁𝗂𝗇𝗀𝗌 𝗌𝖺𝖿𝖾.</blockquote></b>")
    if len(args) == 1:
        return await message.reply_photo(
            START_PIC,
            caption=start_text
        )
    param = args[1]
    is_req = False
    if param.startswith("req_"):
        is_req = True
        param = param[4:]
    try:
        channel_id = decode_channel_id(param)
    except Exception:
        return await message.reply("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗌𝗍𝖺𝗋𝗍 𝗉𝖺𝗋𝖺𝗆𝖾𝗍𝖾𝗋.")
    ch = channels_col.find_one({"_id": channel_id})
    if not ch:
        return await message.reply("𝖳𝗁𝗂𝗌 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗂𝗌 𝗇𝗈𝗍 𝗋𝖾𝗀𝗂𝗌𝗍𝖾𝗋𝖾𝖽 𝗐𝗂𝗍𝗁 𝗍𝗁𝖾 𝖻𝗈𝗍.")
    try:
        if is_req:
            link_name = f"req_{channel_id}_{message.from_user.id}"
            try:
                prev_links = await app.get_chat_invite_links(channel_id, admin_id=app.me.id)
                for l in prev_links:
                    if l.creates_join_request and l.name == link_name:
                        await app.revoke_chat_invite_link(channel_id, l.invite_link)
            except Exception:
                pass
            invite = await app.create_chat_invite_link(
                chat_id=channel_id,
                creates_join_request=True,
                name=link_name
            )
            text = "𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝗍𝗈 𝖩𝗈𝗂𝗇: 𝗉𝗈𝗐𝖾𝗋𝖾𝖽 𝖻𝗒 @AnimeNexusNetwork\n<i>𝖳𝗁𝗂𝗌 𝗅𝗂𝗇𝗄 𝗋𝖾𝗊𝗎𝗂𝗋𝖾𝗌 𝖺𝖽𝗆𝗂𝗇 𝖺𝗉𝗉𝗋𝗈𝗏𝖺𝗅. 𝖮𝗇𝗅𝗒 𝗒𝗈𝗎 𝖼𝖺𝗇 𝗎𝗌𝖾 𝗂𝗍.</i>"
            if 'LINK_PIC' in globals() and LINK_PIC:
                sent = await message.reply_photo(
                    LINK_PIC,
                    caption=text,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("「𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝗍𝗈 𝖩𝗈𝗂𝗇」", url=invite.invite_link)]]
                    )
                )
            else:
                sent = await message.reply(
                    text,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("「𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝗍𝗈 𝖩𝗈𝗂𝗇」", url=invite.invite_link)]]
                    ),
                    disable_web_page_preview=True
                )
            await asyncio.sleep(60)
            try:
                await app.revoke_chat_invite_link(channel_id, invite.invite_link)
            except:
                pass
            try:
                await sent.delete()
            except:
                pass
        else:
            invite = await app.create_chat_invite_link(
                chat_id=channel_id,
                expire_date=datetime.utcnow() + timedelta(minutes=10),
                member_limit=1
            )
            text = "𝖧𝖾𝗋𝖾 𝗂𝗌 𝗒𝗈𝗎𝗋 𝗅𝗂𝗇𝗄! 𝖢𝗅𝗂𝖼𝗄 𝖻𝖾𝗅𝗈𝗐 𝗍𝗈 𝗉𝗋𝗈𝖼𝖾𝖾𝗅: 𝗉𝗈𝗐𝖾𝗋𝖾𝖽 𝖻𝗒 @AnimeNexusNetwork"
            if 'LINK_PIC' in globals() and LINK_PIC:
                sent = await message.reply_photo(
                    LINK_PIC,
                    caption=text,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("「𝖩𝗈𝗂𝗇 𝖢𝗁𝖺𝗇𝗇𝖾𝗅」", url=invite.invite_link)]]
                    )
                )
            else:
                sent = await message.reply(
                    text,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("「𝖩𝗈𝗂𝗇 𝖢𝗁𝖺𝗇𝗇𝖾𝗅」", url=invite.invite_link)]]
                    ),
                    disable_web_page_preview=True
                )
            await asyncio.sleep(60)
            try:
                await app.revoke_chat_invite_link(channel_id, invite.invite_link)
            except:
                pass
            try:
                await sent.delete()
            except:
                pass
    except Exception as e:
        await message.reply(f"𝖥𝖺𝗂𝗅𝖾𝖽 𝗍𝗈 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝖾 𝗂𝗇𝗏𝗂𝗍𝖾: {e}")

# ... all your other handlers (broadcast, stats, etc.) remain unchanged

# Start the Telegram bot
app.run()

# Start aiohttp web server (for hosting platform ping)
async def handle(request):
    return web.Response(text="Bot is running.")

def run_web():
    app_web = web.Application()
    app_web.router.add_get("/", handle)
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app_web, host="0.0.0.0", port=port)

# Start the web server in background thread
threading.Thread(target=run_web).start()
