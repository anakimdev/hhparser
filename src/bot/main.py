import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.bot import configs
from src.bot.handlers import router

class TelegramBot:
    def __init__(self):
        self.bot = Bot(token = configs.TELEGRAM_TOKEN, parse_mode = ParseMode.HTML)
        self.dp = Dispatcher(storage = MemoryStorage())
        self.dp.include_router(router)

    async def main(self):
        await self.bot.delete_webhook(drop_pending_updates = True)
        await self.dp.start_polling(self.bot, allowed_updates = self.dp.resolve_used_update_types())


def start():
    logging.basicConfig(level=logging.INFO)
    tb = TelegramBot()
    asyncio.run(tb.main())

if __name__ == "__main__":
    start()