import datetime
import logging
import os

from aiogram import executor
from aiogram.types import BotCommand

from utils.dispatcher import dp, bot
from utils.regHandler import register_handlers

os.makedirs("logs", exist_ok=True)

logs_path = f"logs/{datetime.datetime.today().strftime('%d-%m-%Y')}.log"

# =====================================#
# --------------logging----------------#
# =====================================#
file_log = logging.FileHandler(logs_path)
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out),
                    format='[%(asctime)s | %(levelname)s]: %(message)s',
                    datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.INFO)

logging.info('\n\n---------------[Bot started!]---------------')


async def setup_bot_commands(*args, **kwargs):
    bot_commands = [
        BotCommand(command="/start", description="♻️ Обновление бота"),
        BotCommand(command="/help", description="🛟 О боте"),
        BotCommand(command="/callall", description="📢 Созвать всех"),
        BotCommand(command="/kick", description="👟 Выгнать из группы")
    ]
    await bot.set_my_commands(bot_commands)


register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, fast=True, skip_updates=True, on_startup=setup_bot_commands)
