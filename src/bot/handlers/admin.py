from aiogram import types, Router, F
from aiogram.types import Message
from aiogram.filters import Command

from src.bot import configs
from src.apies.main import create_data_collector
from src.bot.filters.chat_types import ChatTypeFilter, IsAdmin
from src.bot.keyboards.reply import get_keyboard
from src.bot.response_optimizer import optimization_result

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())
data_collector = create_data_collector()


@admin_router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет, над чем сегодня поработаем", keyboard=get_keyboard())