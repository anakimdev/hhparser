import asyncio
import logging
import os

from dotenv import find_dotenv, load_dotenv

from bot.handlers.company.company_router import company_router
from bot.handlers.vacancies.vacancies_router import vacancies_router
from bot.middlewares.db import DatabaseSessionMiddleware

load_dotenv(find_dotenv())

from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeAllPrivateChats

from bot import configs
from bot.common.bot_cmnd_list import commands_for_users
from bot.handlers.user_private import user_private_router
from bot.handlers.admin import admin_router
# from database.engine import create_db, drop_db, session_maker

ALLOWED_UPDATES = ['message, edited_message', 'callback_query', ]


class TelegramBot:
    def __init__(self):
        self.bot = Bot(token = configs.TELEGRAM_TOKEN, parse_mode = ParseMode.HTML)
        self.dp = Dispatcher(storage = MemoryStorage())
        self.dp.include_routers(admin_router, user_private_router)

    # async def on_startup(self):
    #     # db_active = False
    #     # if db_active:
    #     #     await drop_db()
    #     #
    #     await create_db()
    #
    # async def on_shutdown(self):
    #     print('Бот лег')

    async def main(self):
        # self.dp.startup.register(self.on_startup)
        # self.dp.shutdown.register(self.on_shutdown)
        # self.dp.update.middleware(DatabaseSessionMiddleware(session_pool = session_maker))
        await self.bot.delete_webhook(drop_pending_updates = True)
        # await self.bot.delete_my_commands(scope = types.BotCommandScopeAllPrivateChats())
        # await self.bot.set_my_commands(commands = commands_for_users, scope = types.BotCommandScopeAllPrivateChats())
        await self.dp.start_polling(self.bot, allowed_updates = self.dp.resolve_used_update_types())


def start():
    logging.basicConfig(level = logging.INFO)
    tb = TelegramBot()
    asyncio.run(tb.main())


if __name__ == '__main__':
    start()
