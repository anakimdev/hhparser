from aiogram import types, Router, F
from aiogram.types import Message
from aiogram.filters import Command

from src.bot import configs
from src.apies.main import create_data_collector
from src.bot.filters.chat_types import ChatTypeFilter
from src.bot.response_optimizer import optimization_result

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))
data_collector = create_data_collector()

@user_private_router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу тебе найти работу!")

@user_private_router.message(Command("help"))
async def help_handler(msg: Message):
    await msg.answer("Пытаюсь вывести помощь")

@user_private_router.message(Command("about"))
async def help_handler(msg: Message):
    await msg.answer("Я помощник в поиске вакансий")

@user_private_router.message(Command("payment"))
async def help_handler(msg: Message):
    await msg.answer("Варианты оплаты")

@user_private_router.message(F.text)
async def it(msg: types.Message):
    profession = msg.text.lower().split()
    data = {
        'page': 0,
        'per_page': 3,
        'text': profession,
    }
    results = optimization_result(data_collector.get_vacancies(data))
    await msg.answer(text="Вывожу вакансии")

    num = 0

    for item in results:
        num += 1
        await msg.answer(f"{num}.{item}")

    await msg.answer(text='Чтобы получить ссылку на вакансию введите номер')