from aiogram import types

from utils.dispatcher import bot
from utils.misc import permission, is_admin, openYml, replaceYml, getUserByName


@is_admin
@permission
async def cmd_kick(message: types.Message):
    user = message.from_user
    chat = message.chat
    data = openYml("config.yml")
    usr = message.reply_to_message.from_user

    if usr.id == user.id:
        await message.reply(await replaceYml(data['messages']['moderator']['kickSelf'], ["{name}"], [user.full_name]))
        return False

    try:
        member = await bot.get_chat_member(chat.id, usr.id)
        if member.is_chat_member() or member.is_chat_admin():
            await bot.kick_chat_member(chat.id, usr.id)
            await bot.send_message(chat.id,
                                   await replaceYml(data['messages']['moderator']['userKicked'],
                                                    ["{mention.kicked}", "{mention}"],
                                                    [usr.mention, user.mention]))
        else:
            await message.reply(data['messages']['moderator']['userNotFound'])
    except:
        await message.reply(data['messages']['moderator']['userNotFound'])


@is_admin
@permission
async def cmd_kick_without_reply(message: types.Message):
    user = message.from_user
    chat = message.chat
    args = message.text.split(" ")
    data = openYml("config.yml")

    if not args:
        await message.reply(await replaceYml(data['messages']['moderator']['usernameCorrect'],
                                             ["{name}"],
                                             [user.full_name]))
        return False

    try:
        if args[1].startswith("@"):
            userid = await getUserByName(args[1])
            member = await bot.get_chat_member(chat.id, userid)
            if member.is_chat_member() or member.is_chat_admin():
                await bot.kick_chat_member(chat.id, userid)
                await bot.send_message(chat.id,
                                       await replaceYml(data['messages']['moderator']['userKicked'],
                                                        ["{mention.kicked}", "{mention}"],
                                                        [args[1], user.mention]))
            else:
                await message.reply(data['messages']['moderator']['userNotFound'])

    except:
        await message.reply(data['messages']['moderator']['userNotFound'])
