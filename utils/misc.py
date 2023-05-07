import json
import os
import threading

import yaml
from pyrogram import Client

from databases.datamanger import DatabaseManager
from utils.dispatcher import bot

db = DatabaseManager()


def openYml(name: str):
    with open(name, "r", encoding="UTF-8") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data


async def replaceYml(strr: str, ind: list, outd: list):
    # inD = ["{name}", "{mention.kicked}", "{mention}"]
    # outD = [user.full_name, usr.mention, user.mention]

    for i in range(len(ind)):
        strr = strr.replace(ind[i], outd[i])

    return strr


def permission(func):
    async def wrapper(*args):
        message = args[0]
        chat = message.chat
        botID = await bot.get_me()
        botID = botID['id']
        botID = await bot.get_chat_member(chat.id, botID)

        data = openYml("config.yml")

        permissions = ['can_manage_chat',
                       'can_change_info',
                       'can_delete_messages',
                       'can_invite_users',
                       'can_restrict_members',
                       'can_pin_messages',
                       'can_promote_members',
                       'can_manage_video_chats',
                       'can_manage_voice_chats']

        try:
            for perm in permissions:
                if not botID[perm]:
                    await message.reply(data['messages']['noChatPermission'])
                    return False
        except:
            await message.reply(data['messages']['noChatPermission'])
            return False

        await func(*args)

    return wrapper


def is_admin(func):
    async def wrapper(*args):
        message = args[0]
        user_id = message.from_user.id
        data = openYml("config.yml")
        chat_id = message.chat.id
        member_permission = await bot.get_chat_member(chat_id, user_id)
        if member_permission['status'] != "creator" and member_permission['status'] != "administrator":
            await message.reply(data['messages']['noPermission'])
            return False

        await func(*args)

    return wrapper


async def get_all_members(chat_id):
    data = openYml("negr.yml")
    api_id = data['api_id']
    api_hash = data['api_hash']
    token = data['token']

    app = Client("pyro", api_id=api_id, api_hash=api_hash, bot_token=token)

    async def pyro_main(chat_id):
        async with app:
            os.makedirs("groups", exist_ok=True)
            users = []
            async for member in app.get_chat_members(chat_id):
                user = [member.user.id, member.user.mention, member.user.username]
                users.append(user)
            with open(f'groups/{chat_id}.txt', 'w', encoding="UTF-8") as fw:
                json.dump(users, fw)
            print(f"Поступил запрос на сбор участников чата: {chat_id} || Участники: {users}")
            return users

    return await pyro_main(chat_id)


async def getUserByName(username):
    data = openYml("negr.yml")
    api_id = data['api_id']
    api_hash = data['api_hash']
    token = data['token']

    app = Client("pyro", api_id=api_id, api_hash=api_hash, bot_token=token)

    async def pyro_main(username):
        async with app:
            userid = await app.get_chat(username)
            userid = userid.id

        return userid

    return await pyro_main(username)


def isDialog(func):
    async def wrapper(*args):
        message = args[0]
        usrid = message.from_user.id
        data = openYml("config.yml")
        dialogs = await db.getDialogs(usrid)

        if not dialogs:
            await func(*args)

        else:
            await message.reply(data['messages']['chat']['alreadyInChat'])

    return wrapper


def Dialog(func):
    async def wrapper(*args):
        message = args[0]
        usrid = message.from_user.id
        data = openYml("config.yml")
        dialogs = await db.getDialogs(usrid)

        if dialogs:
            await func(*args)

        else:
            await bot.send_message(usrid, data['messages']['start']['cmdStartPrivate'])

    return wrapper


# async def sendLogs(msg):
#     data = openYml("negr.yml")
#     await
