from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

stor = MemoryStorage()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=stor)