import random

from aiogram import types

from utils.dispatcher import bot
from utils.misc import permission, get_all_members, is_admin, openYml, replaceYml


@is_admin
@permission
async def cmd_call_all(message: types.Message):
    user = message.from_user
    chat = message.chat
    args = message.get_args()
    data = openYml("config.yml")
    emojies = data['callAllEmojies']

    if not args:
        await message.reply(await replaceYml(data['messages']['callAll']['correctUsage'], user))
        return False

    members = await get_all_members(chat.id)
    usr_name = []
    for m in members:
        usr_name.append(m[0])

    mentions = []
    for u in usr_name:
        mentions.append(f'<a href="tg://user?id={u}">{random.choice(emojies)}</a>')

    strEnd = ", ".join(mentions)
    msg = args + "\n\n" + strEnd

    msg = await bot.send_message(chat.id, msg, parse_mode='html')
    await bot.pin_chat_message(chat.id, msg.message_id)
