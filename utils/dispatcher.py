import yaml
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

with open("negr.yml", "r") as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

bot = Bot(token=data["token"])
dp = Dispatcher(bot, storage=MemoryStorage())
