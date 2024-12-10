import asyncio
from telethon import events
from .. import bot as Drone
from telethon.errors import (
    FloodWaitError,
    UserDeactivatedError,
    UserIsBlockedError,
    PeerIdInvalidError,
)
from .. import AUTH, MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

# MongoDB Client
mongo = MongoCli(MONGO_URL)

# Database Collections
chats_db = mongo.chats.chatsdb
users_db = mongo.users.usersdb

# Chat Operations
async def get_chats():
    chat_list = []
    async for chat in chats_db.find({"chat": {"$lt": 0}}):
        chat_list.append(chat['chat'])
    return chat_list

async def add_chat(chat):
    if not await get_chat(chat):
        await chats_db.insert_one({"chat": chat})

async def get_chat(chat):
    return await chats_db.find_one({"chat": chat}) is not None

async def del_chat(chat):
    if await get_chat(chat):
        await chats_db.delete_one({"chat": chat})

# User Operations
async def get_users():
    user_list = []
    async for user in users_db.find({"user": {"$gt": 0}}):
        user_list.append(user['user'])
    return user_list

async def add_user(user):
    if not await get_user(user):
        await users_db.insert_one({"user": user})

async def get_user(user):
    return await users_db.find_one({"user": user}) is not None

async def del_user(user):
    if await get_user(user):
        await users_db.delete_one({"user": user})

@Drone.on(events.NewMessage)
async def save_interaction(event):
    if event.is_group:
        await add_chat(event.chat_id)
    else:
        await add_user(event.sender_id)

# Broadcasting Functionality
@Drone.on(events.NewMessage(incoming=True, pattern="/bcast"))
async def broadcast(event):
    if event.sender_id != AUTH:  # Ensures only the owner can execute this command
        return await event.reply("You are not authorized to use this command.")

    if not event.is_reply:
        return await event.reply("✦ Reply to a message to broadcast it.")

    message = await event.get_reply_message()
    exmsg = await event.reply("✦ Started broadcasting!")

    all_chats = await get_chats()  # Retrieve all chats
    all_users = await get_users()  # Retrieve all users

    done_chats, done_users = 0, 0
    failed_chats, failed_users = 0, 0

    # Broadcast to chats
    for chat in all_chats:
        try:
            await message.forward_to(chat)
            done_chats += 1
            await asyncio.sleep(0.1)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except Exception:
            failed_chats += 1

    # Broadcast to users
    for user in all_users:
        try:
            await message.forward_to(user)
            done_users += 1
            await asyncio.sleep(0.1)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except (UserDeactivatedError, UserIsBlockedError, PeerIdInvalidError):
            failed_users += 1
        except Exception:
            failed_users += 1

    # Summary Report
    if failed_users == 0 and failed_chats == 0:
        await exmsg.edit(
            f"**✦ Successfully broadcasted!**\n\n"
            f"❅ **Chats** ➠ `{done_chats}`\n"
            f"❅ **Users** ➠ `{done_users}`"
        )
    else:
        await exmsg.edit(
            f"**✦ Broadcast completed with some issues!**\n\n"
            f"❅ **Chats** ➠ `{done_chats}`\n"
            f"❅ **Users** ➠ `{done_users}`\n"
            f"❅ **Failed Chats** ➠ `{failed_chats}`\n"
            f"❅ **Failed Users** ➠ `{failed_users}`"
        )


@Drone.on(events.NewMessage(incoming=True, pattern="/cast"))
async def announce(event):
    if event.sender_id != AUTH:  # Ensures only the owner can execute this command
        return await event.reply("You are not authorized to use this command.")

    if not event.is_reply:
        return await event.reply("✦ Reply to a message to announce it.")

    message = await event.get_reply_message()
    all_chats = await get_chats()  # Retrieve all chats
    all_users = await get_users()  # Retrieve all users

    failed_chats, failed_users, done_chats, done_users = 0, 0, 0, 0

    # Announce to chats
    for chat in all_chats:
        try:
            # Send the message content as a new message
            if message.text:
                await Drone.send_message(chat, message.text)
            elif message.media:
                await Drone.send_file(chat, file=message.media, caption=message.text or "")
            await asyncio.sleep(0.1)
            done_chats += 1  # Increment done_chats on successful send
        except Exception:
            failed_chats += 1

    # Announce to users
    for user in all_users:
        try:
            # Send the message content as a new message
            if message.text:
                await Drone.send_message(user, message.text)
            elif message.media:
                await Drone.send_file(user, file=message.media, caption=message.text or "")
            await asyncio.sleep(0.1)
            done_users += 1  # Increment done_users on successful send
        except Exception:
            failed_users += 1

    # Response based on results
    if failed_users == 0 and failed_chats == 0:
        await event.reply(
            f"**✦ Successfully announced!**\n\n"
            f"❅ **Users** ➠ `{done_users}`\n"
            f"❅ **Chats** ➠ `{done_chats}`"
        )
    else:
        await event.reply(
            f"**✦ Announce completed with some issues!**\n\n"
            f"❅ **Chats** ➠ `{done_chats}`\n"
            f"❅ **Users** ➠ `{done_users}`\n\n"
            f"> **✦ Note ➥Some messages couldn't be delivered due to errors.**\n\n"
            f"❅ **Failed Users** ➠ `{failed_users}`\n"
            f"❅ **Failed Chats** ➠ `{failed_chats}`"
        )
