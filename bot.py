# bot.py
from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
from datetime import datetime
import time
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, ADMINS
from utils import encode_channel_id, decode_channel_id

app = Client("invite_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URI)
db = mongo['invite_bot']
users_col = db['users']
channels_col = db['channels']

# Save user on /start
@app.on_message(filters.command("start"))
async def start_handler(_, message: Message):
    users_col.update_one({"_id": message.from_user.id}, {"$set": {"name": message.from_user.first_name}}, upsert=True)
    
    args = message.text.split(" ", 1)
    if len(args) == 1:
        return await message.reply("Welcome!\n\nAvailable Commands:\n/start - Start the bot\n/broadcast - Broadcast a message\n/users - List all users\n/channelpost - Get temporary join link\n/reqpost - Get request join link\n/setchannel - Register a channel\n/delchannel - Unlink a channel\n/stats - Bot usage stats")

    try:
        encoded = args[1]
        channel_id = decode_channel_id(encoded)
    except Exception:
        return await message.reply("Invalid start parameter.")

    ch = channels_col.find_one({"_id": channel_id})
    if not ch:
        return await message.reply("This channel is not registered with the bot.")

    try:
        invite = await app.create_chat_invite_link(
            chat_id=channel_id,
            expire_date=int(time.time()) + 600,
            member_limit=1
        )
        await message.reply(f"Here is your temporary join link:\n{invite.invite_link}\n(This will expire in 10 minutes)")
    except Exception as e:
        await message.reply(f"Failed to generate invite: {e}")

# Broadcast
@app.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast it.")

    users = users_col.find()
    success, failed = 0, 0
    for user in users:
        try:
            await app.copy_message(user['_id'], message.chat.id, message.reply_to_message.id)
            success += 1
        except:
            failed += 1
    await message.reply(f"Broadcast completed.\n✅ Sent: {success}\n❌ Failed: {failed}")

# List users
@app.on_message(filters.command("users") & filters.user(ADMINS))
async def users_list(_, message: Message):
    count = users_col.count_documents({})
    await message.reply(f"Total users: {count}")

# Set channel
@app.on_message(filters.command("setchannel") & filters.user(ADMINS))
async def set_channel(_, message: Message):
    if len(message.command) != 2:
        return await message.reply("Usage: /setchannel @channelusername")

    username = message.command[1].lstrip("@")
    try:
        chat = await app.get_chat(username)
        if not chat.id:
            raise Exception("Invalid chat")
        channels_col.update_one({"_id": chat.id}, {"$set": {"username": chat.username}}, upsert=True)
        await message.reply(f"Channel @{chat.username} registered.")
    except Exception as e:
        await message.reply(f"Error: {e}")

# Delete channel
@app.on_message(filters.command("delchannel") & filters.user(ADMINS))
async def delete_channel(_, message: Message):
    if len(message.command) != 2:
        return await message.reply("Usage: /delchannel @channelusername")

    username = message.command[1].lstrip("@")
    chat = await app.get_chat(username)
    result = channels_col.delete_one({"_id": chat.id})
    if result.deleted_count:
        await message.reply(f"Channel @{username} removed.")
    else:
        await message.reply("Channel not found.")

# Generate temporary link
@app.on_message(filters.command("channelpost") & filters.user(ADMINS))
async def channel_post(_, message: Message):
    registered = channels_col.find()
    links = []
    async for ch in registered:
        try:
            invite = await app.create_chat_invite_link(
                chat_id=ch['_id'],
                expire_date=int(time.time()) + 600,
                member_limit=1
            )
            encoded = encode_channel_id(ch['_id'])
            full_link = f"[Click here for @{ch['username']}](https://t.me/{app.me.username}?start={encoded})"
            links.append(full_link)
        except Exception as e:
            links.append(f"❌ @{ch['username']}: {e}")

    await message.reply("\n".join(links), disable_web_page_preview=True)

# Generate join request link
@app.on_message(filters.command("reqpost") & filters.user(ADMINS))
async def req_post(_, message: Message):
    registered = channels_col.find()
    links = []
    async for ch in registered:
        try:
            chat = await app.get_chat(ch['_id'])
            invite_link = chat.invite_link or await app.export_chat_invite_link(ch['_id'])
            links.append(f"[Request Join @{ch['username']}]({invite_link})")
        except Exception as e:
            links.append(f"❌ @{ch['username']}: {e}")

    await message.reply("\n".join(links), disable_web_page_preview=True)

# Stats
@app.on_message(filters.command("stats") & filters.user(ADMINS))
async def stats(_, message: Message):
    user_count = users_col.count_documents({})
    channel_count = channels_col.count_documents({})
    await message.reply(f"👥 Users: {user_count}\n📡 Channels: {channel_count}")

app.run()
