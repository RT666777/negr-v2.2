from aiogram import types

from databases.datamanger import DatabaseManager
from keyboards.default import start_private_keyboard
from utils.dispatcher import bot
from utils.misc import isDialog, openYml, Dialog

db = DatabaseManager()


@isDialog
async def cmd_search(message: types.Message):
    user = message.from_user
    chat = message.chat
    data = openYml("config.yml")

    dialog = await db.getNullDialogs()
    if dialog:
        await db.updateDialogs(2, user.id)
        await bot.send_message(chat.id, data['messages']['chat']['userFound'])
        await bot.send_message(dialog[0], data['messages']['chat']['userFound'])

    else:
        await db.replaceDialogs(user.id, None)
        await bot.send_message(chat.id, data['messages']['chat']['userInQueue'])


@Dialog
async def cmd_forward_message(message: types.Message):
    user = message.from_user
    chat = message.chat

    dialog = await db.getDialogs(user.id)
    dialog = dialog[0]

    userTo = dialog[1]
    if userTo == user.id:
        userTo = dialog[2]

    await bot.copy_message(userTo, user.id, message.message_id)


@Dialog
async def cmd_stop_dialog(message: types.Message):
    user = message.from_user
    chat = message.chat
    data = openYml("config.yml")

    dialog = await db.getDialogs(user.id)
    dialog = dialog[0]

    userTo = dialog[1]
    if userTo == user.id:
        userTo = dialog[2]

    await bot.send_message(userTo, data['messages']['chat']['dialogStopped'], reply_markup=start_private_keyboard)

    await db.stopDialog(user.id)
    await bot.send_message(chat.id, data['messages']['chat']['dialogStopped'], reply_markup=start_private_keyboard)
