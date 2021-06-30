import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.bear import register_handlers_bear
from handlers.common import register_handlers_common

token = os.getenv("TOKEN")
print(token)
logger = logging.getLogger(__name__)
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())


async def set_commands(bot: Bot):
    commands = [BotCommand(command="/help", description="Помощь")]
    await bot.set_my_commands(commands)


async def main_bot():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    register_handlers_common(dp)
    register_handlers_bear(dp)
    await set_commands(bot)
    await dp.start_polling()
