import re

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from src.bot.filters.chat_types import ChatTypeFilter
from src.bot.keyboards.inline import get_callback_btns
from src.bot.keyboards.reply import get_keyboard
from src.bot.optimizers.optimizer import get_vacancy, get_vacancies

vacancies_router = Router()
vacancies_router.message.filter(ChatTypeFilter(['private']))

USERS_KEYBOARD = get_keyboard('Найти вакансии', 'Статистика', 'О нас', 'Варианты оплаты', 'Помощь')


class SearchRequest(StatesGroup):
    name = State()
    salary = State()
    region = State()
    per_page = State()
    num = State()
    page = State()

    texts = {
        "SearchRequest:name": "Введите профессию заново",
        "SearchRequest:salary": "Введите зарплату заново",
        "SearchRequest:region": "Введите регион заново",
    }


# Searching FSM

@vacancies_router.message(Command('search'))
@vacancies_router.message(StateFilter(None), F.text.casefold() == 'найти вакансии')
async def start_search_handler(msg: Message, state: FSMContext):
    await msg.answer('💻 Введите название профессии')
    await state.set_state(SearchRequest.name)


@vacancies_router.message(StateFilter('*'), Command('cancel'))
@vacancies_router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def cancel_handler(msg: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await msg.answer('Все действия отменены', reply_markup=USERS_KEYBOARD)


@vacancies_router.message(StateFilter('*'), Command('back'))
@vacancies_router.message(StateFilter('*'), F.text.casefold() == 'назад')
async def step_back_handler(msg: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == SearchRequest.name:
        await msg.answer('Предыдущего шага не предусмотрено. Введите название профессии или нажмите "отмена"')
        return

    previous = None
    for step in SearchRequest.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await msg.answer(f"Вы вернулись к прошлому шагу \n{SearchRequest.texts[previous.state]}")
            return
        previous = step


@vacancies_router.message(StateFilter(SearchRequest.name), F.text)
async def search_name_handler(msg: Message, state: FSMContext):
    if len(msg.text) > 100:
        await msg.answer('Введите профессию заново')
        return
    await msg.delete()
    await state.update_data(name=msg.text)
    await msg.answer('💰 Введите среднюю ожидаемую зарплату')
    await state.set_state(SearchRequest.salary)


@vacancies_router.message(StateFilter(SearchRequest.salary), F.text)
async def search_salary_handler(msg: Message, state: FSMContext):
    pattern = '\d+'
    if not re.fullmatch(pattern, msg.text):
        await msg.answer('Введите зарплату заново')
        return
    await state.update_data(salary=msg.text)
    await msg.answer('🌐 Введите регион для работы.\nПо умолчанию, "Все"')
    await state.set_state(SearchRequest.region)


@vacancies_router.message(StateFilter(SearchRequest.region), F.text)
async def search_region_handler(msg: Message, state: FSMContext):
    await state.update_data(region=msg.text, page='0', num='0')
    await msg.answer('🔢 Введите количество вакансий на странице')
    await state.set_state(SearchRequest.per_page)


@vacancies_router.message(StateFilter(SearchRequest.per_page), F.text)
async def search_vacancies_handler(msg: Message, state: FSMContext):
    await state.update_data(per_page=msg.text, page=0, num=0)
    await make_vacancies_list(msg, await state.get_data())


@vacancies_router.callback_query(F.data.startswith('full_vacancy_'))
async def show_full_vacancy(callback: types.CallbackQuery):
    res = callback.data.split('_')
    number = res[2]
    link = res[3]
    vacancy_id = link.split('/')[-1]

    vacancy = await get_vacancy(vacancy_id)

    await callback.answer('')
    await callback.message.answer(f"{number}. {vacancy.company_name}\n\n{vacancy.description}",
                                  reply_markup=get_callback_btns(btns={
                                      "✉ Показать ссылку": f"link_{number}_{link}"
                                  }))


@vacancies_router.callback_query(F.data.startswith('link_'))
async def show_link(callback: types.CallbackQuery):
    res = callback.data.split('_')
    number = res[1]
    link = res[2]

    await callback.answer('')
    await callback.message.answer(f'Ccылка для вакансии № {number}: {link}')


@vacancies_router.callback_query(F.data.startswith(('prev_vacancies_', 'next_vacancies_')))
async def search_paginator_vacancies_handler(callback: types.CallbackQuery, state: FSMContext):
    res = callback.data.split('_')

    await state.update_data(page=res[2], num=res[3])
    await make_vacancies_list(callback.message, await state.get_data())
    await callback.answer('')


async def make_vacancies_list(msg: Message, data: dict[str]):
    current_page = int(data.get('page'))
    per_page = int(data.get('per_page', 5))

    request_data = {
        'page': current_page,
        'per_page': per_page,
        'text': data.get('name'),
        'salary': int(data.get('salary')),
        'region': data.get('region')
    }

    await msg.answer(text="Вывожу вакансии")
    vacancies = await get_vacancies(request_data)

    num = (current_page * per_page)

    for vacancy in vacancies:
        num += 1
        link = vacancy.link
        text = (f'{num}. {vacancy.company_name}'
                f'\n\n💼 {vacancy.experience}'
                f'\n\n💵 {vacancy.salary}'
                f'\n\n📚 {vacancy.description}'
                f'\n\n⚙ {vacancy.key_skills}')


        await msg.answer(text, reply_markup=get_callback_btns(btns={
                             "✉ Ссылка": f"link_{num}_{link}",
                             "📄 Полное описание": f"full_vacancy_{num}_{link}",
                             "👔 О компании": f"company_{vacancy.company_name}"
                         }, sizes=(1, 1, 1)))

    await make_nagivation_buttons(msg, current_page, num)


async def make_nagivation_buttons(msg: Message, current_page: int, num: int):
    if current_page == 0:
        await msg.answer('Что делаем дальше?', reply_markup=get_callback_btns(btns={
            '⤴ Вернуться в главное меню': f"start",
            "➡ Вперед": f"next_vacancies_{current_page + 1}_{num}"
        }, sizes=(1, 2)))
    else:
        await msg.answer('Что делаем дальше?', reply_markup=get_callback_btns(btns={
            "⤴ Вернуться в главное меню": f"start",
            "⬅ Назад": f"prev_vacancies_{current_page - 1}_{num}",
            "➡ Вперед": f"next_vacancies_{current_page + 1}_{num}"
        }, sizes=(1, 2)))
