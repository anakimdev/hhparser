import time

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup

from src.apies.main import create_hunter_collector
from src.bot.filters.chat_types import ChatTypeFilter
from src.bot.keyboards.inline import get_callback_btns
from src.bot.keyboards.reply import get_keyboard
from src.bot.optimizers.optimizer import get_vacancies, get_vacancy, get_company_info

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))
vacancy_collector = create_hunter_collector()

USERS_KEYBOARD = get_keyboard('Найти вакансии', 'Статистика', 'О нас', 'Варианты оплаты', 'Помощь')


class SearchRequest(StatesGroup):
    name = State()
    salary = State()
    region = State()

    texts = {
        "SearchRequest:name": "Введите профессию заново",
        "SearchRequest:salary": "Введите зарплату заново",
        "SearchRequest:region": "Введите регион заново",
    }


# Common commands
@user_private_router.message(Command("start"))
@user_private_router.message(StateFilter(None), F.text().casefold == 'старт')
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу тебе найти работу!", reply_markup=USERS_KEYBOARD)


@user_private_router.message(Command("help"))
@user_private_router.message(StateFilter(None), F.text.casefold == 'помощь')
async def help_handler(msg: Message):
    await msg.answer("Пытаюсь вывести помощь")


@user_private_router.message(Command("about"))
@user_private_router.message(StateFilter(None), F.text.casefold == 'о нас')
async def about_handler(msg: Message):
    await msg.answer("Здесь будет информация о боте")


@user_private_router.message(Command("payment"))
async def payments_handler(msg: Message):
    await msg.answer("Здесь будет информация о вариантах оплаты")


# Searching FSM
@user_private_router.message(Command('search'))
@user_private_router.message(StateFilter(None), F.text.casefold() == 'найти вакансии')
async def start_search_handler(msg: Message, state: FSMContext):
    await msg.answer('Введите название профессии')
    await state.set_state(SearchRequest.name)


@user_private_router.message(StateFilter('*'), Command('cancel'))
@user_private_router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def cancel_handler(msg: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await msg.answer('Все действия отменены', reply_markup=USERS_KEYBOARD)


@user_private_router.message(StateFilter('*'), Command('back'))
@user_private_router.message(StateFilter('*'), F.text.casefold() == 'назад')
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


@user_private_router.message(StateFilter(SearchRequest.name), F.text)
async def search_name_handler(msg: Message, state: FSMContext):
    if len(msg.text) > 100:
        await msg.answer('Введите профессию заново')
        return
    await state.update_data(name=msg.text)
    await msg.answer('Введите среднюю ожидаемую зарплату')
    await state.set_state(SearchRequest.salary)


@user_private_router.message(StateFilter(SearchRequest.salary), F.text)
async def search_salary_handler(msg: Message, state: FSMContext):
    await state.update_data(salary=msg.text)
    await msg.answer('Введите регион для работы.\nДля того, чтобы указать все, напишите "Все"')
    await state.set_state(SearchRequest.region)


@user_private_router.message(StateFilter(SearchRequest.region), F.text)
async def search_region_handler(msg: Message, state: FSMContext):
    await state.update_data(region=msg.text)
    await msg.answer('Начинаю поиск. Ожидайте')
    user_data = await state.get_data()

    page = 0
    request_data = {
        'page': page,
        'per_page': 5,
        'text': user_data.get('name'),
        'salary': int(user_data.get('salary')),
        'region': user_data.get('region')
    }

    vacancies = await get_vacancies(request_data)
    await msg.answer(text="Вывожу вакансии")

    num = 0

    for vacancy in vacancies:
        num += 1
        data = str(vacancy)
        link = vacancy.get_link()

        await msg.answer(f"{num}.{data}",
                         reply_markup=get_callback_btns(btns={
                             "Показать полное описание": f"show_{num}_{link}",
                             "Показать ссылку": f"link_{num}_{link}",
                             "Показать информацию о компании": f"get_company_{vacancy.get_name()}"
                         }))

    await msg.answer('Что делаем дальше?', reply_markup=get_callback_btns(btns={
        "Назад": f"back_{page - 1}",
        "Вперед": f"next_{page + 1}",
        "Уведомлять о публикациях": f"watch_{msg.from_user}",
        "Вернуться в главное меню": f"start"
    }))
    await state.clear()


@user_private_router.callback_query(F.data.startswith('show_'))
async def show_full_vacancy(callback: types.CallbackQuery):
    res = callback.data.split('_')
    number = res[1]
    link = res[2]
    vacancy_id = link.split('/')[-1]

    vacancy = await get_vacancy(vacancy_id)

    await callback.answer('')
    await callback.message.answer(f"{number}. {vacancy.get_name()}\n\n{str(vacancy)}",
                                  reply_markup=get_callback_btns(btns={
                                      "Показать ссылку": f"link_{number}_{link}"
                                  }))


@user_private_router.callback_query(F.data.startswith('link_'))
async def show_link(callback: types.CallbackQuery):
    res = callback.data.split('_')
    number = res[1]
    link = res[2]

    await callback.answer('')
    await callback.message.answer(f'Ccылка для вакансии № {number}: {link}')


@user_private_router.callback_query(F.data.startswith('get_company_'))
async def get_company(callback: types.CallbackQuery):
    res = callback.data.split('_')
    name = res[2].split(': ')[1]

    await callback.message.answer('Ищу ИНН')
    data = await get_company_info(name)

    commmon_data = '\n'.join(data.get('common_data'))
    requisites = '\n'.join(data.get('requisites'))
    background_data = '\n'.join(data.get('background_data'))

    card_of_company = (
        f'Общая информация\n\n{commmon_data}\n\nРеквизиты компании\n\n{requisites}\n\n'
        f'Дополнительные данные\n\n{background_data}')

    await callback.message.answer('Делаю запрос на сайт ФНС')
    await callback.message.answer(card_of_company)
