from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from src.bot import configs
from src.apies.main import create_data_collector

router = Router()
data_collector = create_data_collector()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.delete()
    await msg.answer("Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение")

@router.message(Command("help"))
async def help_handler(msg: Message):
    await msg.delete()
    await msg.answer(text = configs.HELP_TEXT)

@router.message()
async def it(msg: types.Message):
    profession = msg.text.lower().split()
    data = {
        'page': 0,
        'per_page': 10,
        'text': profession,
    }
    response_data = data_collector.get_vacancies(data)




