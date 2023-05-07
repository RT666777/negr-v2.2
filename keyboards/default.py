from aiogram import types

start_private_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton("👾 Поиск собеседника")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
