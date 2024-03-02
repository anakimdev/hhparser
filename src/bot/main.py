import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeAllPrivateChats

from src.bot import configs
from src.bot.common.bot_cmnd_list import commands_for_users
from src.bot.handlers.user_private import user_private_router
from src.bot.handlers.admin import admin_router


ALLOWED_UPDATES = ['message, edited_message']


class TelegramBot:
    def __init__(self):
        self.bot = Bot(token = configs.TELEGRAM_TOKEN, parse_mode = ParseMode.HTML)
        self.dp = Dispatcher(storage = MemoryStorage())
        self.dp.include_routers(admin_router, user_private_router, )

    async def main(self):
        await self.bot.delete_webhook(drop_pending_updates = True)
        # await self.bot.delete_my_commands(scope = types.BotCommandScopeAllPrivateChats())
        await self.bot.set_my_commands(commands = commands_for_users, scope = types.BotCommandScopeAllPrivateChats())
        await self.dp.start_polling(self.bot, allowed_updates = ALLOWED_UPDATES)

def start():
    logging.basicConfig(level=logging.INFO)
    tb = TelegramBot()
    asyncio.run(tb.main())

if __name__ == "__main__":
    start()