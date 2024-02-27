from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from src.bot import configs

router = Router()

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
    city = msg.text.strip().lower()
    print(city)


