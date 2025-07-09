# bot.py
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

app = Client("invite_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URI)
db = mongo['invite_bot']
users_col = db['users']
channels_col = db['channels']

@app.on_message(filters.command("start"))
async def start_handler(_, message: Message):
    users_col.update_one({"_id": message.from_user.id}, {"$set": {"name": message.from_user.first_name}}, upsert=True)
    args = message.text.split(" ", 1)
    start_text = ("<b><blockquote>𝖡𝖺𝗄𝗄𝖺 {mention}!\n\n𝖨’𝗆 𝗍𝗁𝖾 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖫𝗂𝗇𝗄 𝖡𝗈𝗍 — 𝖨 𝖼𝗋𝖾𝖺𝗍𝖾 𝗌𝗆𝖺𝗋𝗍 𝗋𝖾𝖽𝗂𝗋𝖾𝖼𝗍 𝗅𝗂𝗇𝗄𝗌 𝖿𝗈𝗋 𝗒𝗈𝗎𝗋 𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝖼𝗁𝖺𝗇𝗇𝖾𝗅𝗌 𝗍𝗈 𝗁𝖾𝗅𝗉 𝖺𝗏𝗈𝗂𝖽 𝖼𝗈𝗉𝗒𝗋𝗂𝗀𝗁𝗍 𝗉𝗋𝗈𝖻𝗅𝖾𝗆𝗌 𝖺𝗇𝖽 𝗄𝖾𝖾𝗉 𝗍𝗁𝗂𝗇𝗀𝗌 𝗌𝖺𝖿𝖾.</blockquote></b>")
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
            text = "𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝗍𝗈 𝖩𝗈𝗂𝗇: 𝗉𝗈𝗐𝖾𝗋𝖾𝖽 𝖻𝗒 @Bots_Nation\n<i>𝖳𝗁𝗂𝗌 𝗅𝗂𝗇𝗄 𝗋𝖾𝗊𝗎𝗂𝗋𝖾𝗌 𝖺𝖽𝗆𝗂𝗇 𝖺𝗉𝗉𝗋𝗈𝗏𝖺𝗅. 𝖮𝗇𝗅𝗒 𝗒𝗈𝗎 𝖼𝖺𝗇 𝗎𝗌𝖾 𝗂𝗍.</i>"
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
            await asyncio.sleep(600)
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
            text = "𝖧𝖾𝗋𝖾 𝗂𝗌 𝗒𝗈𝗎𝗋 𝗅𝗂𝗇𝗄! 𝖢𝗅𝗂𝖼𝗄 𝖻𝖾𝗅𝗈𝗐 𝗍𝗈 𝗉𝗋𝗈𝖼𝖾𝖾𝗅: 𝗉𝗈𝗐𝖾𝗋𝖾𝖽 𝖻𝗒 @Bots_Nation"
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
            await asyncio.sleep(600)
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

@app.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗍𝗈 𝖻𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝗂𝗍.")

    users = users_col.find()
    success, failed = 0, 0
    for user in users:
        try:
            await app.copy_message(user['_id'], message.chat.id, message.reply_to_message.id)
            success += 1
        except:
            failed += 1
    await message.reply(f"𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽.\n𝖲𝖾𝗇𝗍: {success}\n𝖥𝖺𝗂𝗅𝖾𝖽: {failed}")

@app.on_message(filters.command("users") & filters.user(ADMINS))
async def users_list(_, message: Message):
    count = users_col.count_documents({})
    await message.reply(f"𝖳𝗈𝗍𝖺𝗅 𝗎𝗌𝖾𝗋𝗌: {count}")

@app.on_message(filters.command("setchannel") & filters.user(ADMINS))
async def set_channel(_, message: Message):
    if len(message.command) != 2:
        return await message.reply("𝖴𝗌𝖺𝗀𝖾: /setchannel @username 𝗈𝗋 /setchannel -1001234567890")

    target = message.command[1]
    if target.startswith("@"):
        chat_ref = target
    else:
        try:
            chat_ref = int(target)
        except ValueError:
            return await message.reply("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖼𝗁𝖺𝗇𝗇𝖾𝗅/𝗀𝗋𝗈𝗎𝗉 𝗂𝖽𝖾𝗇𝗍𝗂𝖿𝗂𝖾𝗋.")

    try:
        chat = await app.get_chat(chat_ref)
        if chat.type not in [ChatType.CHANNEL, ChatType.SUPERGROUP, ChatType.GROUP]:
            return await message.reply(
                f"𝖴𝗇𝗌𝗎𝗉𝗉𝗈𝗋𝗍𝖾𝖽 𝖼𝗁𝖺𝗍 𝗍𝗒𝗉𝖾: `{chat.type}`.\n"
                "𝖮𝗇𝗅𝗒 𝖼𝗁𝖺𝗇𝗇𝖾𝗅𝗌, 𝗀𝗋𝗈𝗎𝗉𝗌, 𝖺𝗇𝖽 𝗌𝗎𝗉𝖾𝗋𝗀𝗋𝗈𝗎𝗉𝗌 𝖺𝗋𝖾 𝗌𝗎𝗉𝗉𝗈𝗋𝗍𝖾𝖽.\n"
                "𝖬𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗂𝗌 𝖺 𝗆𝖾𝗆𝖻𝖾𝗋/𝖺𝖽𝗆𝗂𝗇 𝗈𝖿 𝗍𝗁𝖾 𝗍𝖺𝗋𝗀𝖾𝗍."
            )
        channels_col.update_one(
            {"_id": chat.id},
            {"$set": {
                "username": chat.username,
                "type": str(chat.type),
                "title": chat.title
            }},
            upsert=True
        )
        await message.reply(
            f"{chat.type.name.title()} '{chat.title}' 𝗋𝖾𝗀𝗂𝗌𝗍𝖾𝗋𝖾𝖽.\n"
            f"𝖨𝖣: `{chat.id}`\n"
            f"𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾: @{chat.username if chat.username else 'N/A'}"
        )
    except Exception as e:
        await message.reply(
            f"𝖤𝗋𝗋𝗈𝗋: {e}\n"
            "𝖬𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗂𝗌 𝖺 𝗆𝖾𝗆𝖻𝖾𝗋/𝖺𝖽𝗆𝗂𝗇 𝗈𝖿 𝗍𝗁𝖾 𝗍𝖺𝗋𝗀𝖾𝗍 𝖺𝗇𝖽 𝗍𝗁𝖾 𝖨𝖣/𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾 𝗂𝗌 𝖼𝗈𝗋𝗋𝖾𝖼𝗍."
        )

@app.on_message(filters.command("delchannel") & filters.user(ADMINS))
async def delete_channel(_, message: Message):
    if len(message.command) != 2:
        return await message.reply("𝖴𝗌𝖺𝗀𝖾: /delchannel @username 𝗈𝗋 /delchannel -1001234567890")

    target = message.command[1]
    if target.startswith("@"):
        chat_ref = target
    else:
        try:
            chat_ref = int(target)
        except ValueError:
            return await message.reply("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖼𝗁𝖺𝗇𝗇𝖾𝗅/𝗀𝗋𝗈𝗎𝗉 𝗂𝖽𝖾𝗇𝗍𝗂𝖿𝗂𝖾𝗋.")

    try:
        chat = await app.get_chat(chat_ref)
        result = channels_col.delete_one({"_id": chat.id})
        if result.deleted_count:
            await message.reply(f"{chat.type.name.title()} '{chat.title}' 𝗋𝖾𝗆𝗈𝗏𝖾𝖽.")
        else:
            await message.reply("𝖢𝗁𝖺𝗇𝗇𝖾𝗅/𝗀𝗋𝗈𝗎𝗉 𝗇𝗈𝗍 𝖿𝗈𝗎𝗇𝖽.")
    except Exception as e:
        await message.reply(f"Error: {e}")

@app.on_message(filters.command("channelpost") & filters.user(ADMINS))
async def channel_post(_, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) == 2:
        target = args[1]
        if target.startswith("@"):
            ch = channels_col.find_one({"username": target[1:]})
        else:
            try:
                ch = channels_col.find_one({"_id": int(target)})
            except Exception:
                return await message.reply("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖼𝗁𝖺𝗇𝗇𝖾𝗅/𝗀𝗋𝗈𝗎𝗉 𝗂𝖽𝖾𝗇𝗍𝗂𝖿𝗂𝖾𝗋.")
        if not ch:
            return await message.reply("𝖢𝗁𝖺𝗇𝗇𝖾𝗅/𝗀𝗋𝗈𝗎𝗉 𝗇𝗈𝗍 𝖿𝗈𝗎𝗇𝖽.")
        try:
            encoded = encode_channel_id(ch['_id'])
            link = f"https://t.me/{app.me.username}?start={encoded}"
            await message.reply(
                f"𝖳𝖾𝗆𝗉𝗈𝗋𝖺𝗋𝗒 𝗃𝗈𝗂𝗇 𝗅𝗂𝗇𝗄 𝖿𝗈𝗋 <b>{ch.get('title', ch.get('username', ch['_id']))}</b>:\n"
                f"<a href='{link}'>𝖢𝗅𝗂𝖼𝗄 𝗁𝖾𝗋𝖾</a>",
                disable_web_page_preview=True
            )
        except Exception as e:
            await message.reply(f"❌ {ch.get('username', ch.get('title', ch['_id']))}: {e}")
        return
    registered = channels_col.find()
    links = []
    for ch in registered:
        try:
            encoded = encode_channel_id(ch['_id'])
            link = f"https://t.me/{app.me.username}?start={encoded}"
            links.append(f"<b>{ch.get('title', ch.get('username', ch['_id']))}</b>: <a href='{link}'>𝖢𝗅𝗂𝖼𝗄 𝗁𝖾𝗋𝖾</a>")
        except Exception as e:
            links.append(f"❌ {ch.get('username', ch.get('title', ch['_id']))}: {e}")
    await message.reply("\n".join(links), disable_web_page_preview=True)

@app.on_message(filters.command("reqpost") & filters.user(ADMINS))
async def req_post(_, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) == 2:
        target = args[1]
        if target.startswith("@"):
            ch = channels_col.find_one({"username": target[1:]})
        else:
            try:
                ch = channels_col.find_one({"_id": int(target)})
            except Exception:
                return await message.reply("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖼𝗁𝖺𝗇𝗇𝖾𝗅/𝗀𝗋𝗈𝗎𝗉 𝗂𝖽𝖾𝗇𝗍𝗂𝖿𝗂𝖾𝗋.")
        if not ch:
            return await message.reply("𝖢𝗁𝖺𝗇𝗇𝖾𝗅/𝗀𝗋𝗈𝗎𝗉 𝗇𝗈𝗍 𝖿𝗈𝗎𝗇𝖽.")
        try:
            encoded = encode_channel_id(ch['_id'])
            link = f"https://t.me/{app.me.username}?start=req_{encoded}"
            await message.reply(
                f"𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝗃𝗈𝗂𝗇 𝗅𝗂𝗇𝗄 𝖿𝗈𝗋 <b>{ch.get('title', ch.get('username', ch['_id']))}</b> (𝗋𝖾𝗊𝗎𝗂𝗋𝖾𝗌 𝖺𝖽𝗆𝗂𝗇 𝖺𝗉𝗉𝗋𝗈𝗏𝖺𝗅):\n"
                f"<a href='{link}'>𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝗍𝗈 𝖩𝗈𝗂𝗇</a>\n\n"
                f"<i>𝖬𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 '𝖠𝗉𝗉𝗋𝗈𝗏𝖾 𝗇𝖾𝗐 𝗆𝖾𝗆𝖻𝖾𝗋𝗌' 𝗂𝗌 𝖾𝗇𝖺𝖻𝗅𝖾𝖽 𝗂𝗇 𝗍𝗁𝖾 𝖼𝗁𝖺𝗇𝗇𝖾𝗅/𝗀𝗋𝗈𝗎𝗉 𝗌𝖾𝗍𝗍𝗂𝗇𝗀𝗌 𝖿𝗈𝗋 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝗌 𝗍𝗈 𝗐𝗈𝗋𝗄.</i>",
                disable_web_page_preview=True
            )
        except Exception as e:
            await message.reply(f"❌ {ch.get('username', ch.get('title', ch['_id']))}: {e}")
        return
    registered = channels_col.find()
    links = []
    for ch in registered:
        try:
            encoded = encode_channel_id(ch['_id'])
            link = f"https://t.me/{app.me.username}?start=req_{encoded}"
            links.append(
                f"<b>{ch.get('title', ch.get('username', ch['_id']))}</b>: <a href='{link}'>𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝗍𝗈 𝖩𝗈𝗂𝗇</a> (𝗋𝖾𝗊𝗎𝗂𝗋𝖾𝗌 𝖺𝖽𝗆𝗂𝗇 𝖺𝗉𝗉𝗋𝗈𝗏𝖺𝗅)"
            )
        except Exception as e:
            links.append(f"❌ {ch.get('username', ch.get('title', ch['_id']))}: {e}")
    await message.reply("\n".join(links) + "\n\n<i>𝖬𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 '𝖠𝗉𝗉𝗋𝗈𝗏𝖾 𝗇𝖾𝗐 𝗆𝖾𝗆𝖻𝖾𝗋𝗌' 𝗂𝗌 𝖾𝗇𝖺𝖻𝗅𝖾𝖽 𝗂𝗇 𝗍𝗁𝖾 𝖼𝗁𝖺𝗇𝗇𝖾𝗅/𝗀𝗋𝗈𝗎𝗉 𝗌𝖾𝗍𝗍𝗂𝗇𝗀𝗌 𝖿𝗈𝗋 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝗌 𝗍𝗈 𝗐𝗈𝗋𝗄.</i>", disable_web_page_preview=True)

@app.on_message(filters.command("stats") & filters.user(ADMINS))
async def stats(_, message: Message):
    user_count = users_col.count_documents({})
    channel_count = channels_col.count_documents({})
    await message.reply(f"𝖴𝗌𝖾𝗋𝗌: {user_count}\n𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌: {channel_count}")

app.run()



from asyncio import web

async def health_check(request):
    return web.Response(text="OK")

async def run_health_server():
    app = web.Application()
    app.router.add_get("/healthz", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
