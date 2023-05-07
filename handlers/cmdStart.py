from aiogram import types

from utils.dispatcher import bot
from utils.misc import openYml, replaceYml, permission
from keyboards.default import start_private_keyboard


async def cmd_start_private(message: types.Message):
    user = message.from_user
    chat = message.chat
    data = openYml("config.yml")

    msg = await replaceYml(data['messages']['start']['cmdStartPrivate'],
                                            ["{name}"],
                                            [user.full_name])

    await bot.send_message(chat.id, msg, reply_markup=start_private_keyboard)


@permission
async def cmd_start_public(message: types.Message):
    user = message.from_user
    chat = message.chat

    await message.reply("Бот работает!")
    print(chat.id)


async def cmd_help(message: types.Message):
    data = openYml("config.yml")
    await message.reply(data['messages']['help'])
