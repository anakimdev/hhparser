from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup

from src.apies.main import create_data_collector
from src.bot.filters.chat_types import ChatTypeFilter, IsAdmin
from src.bot.keyboards.reply import get_keyboard
from src.bot.optimizers.optimizer import get_areas

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())
data_collector = create_data_collector()

ADMIN_KEYBOARD = get_keyboard('Просмотреть статистику', 'Выполнить запрос', 'Войти как пользователь', 'Удалить')
ADMIN_DICTIONARY_KEYBOARD = get_keyboard('Справочник полей', 'Справочник ключевых навыков', 'Справочник стран',
    'Дерево регионов', 'Справочник районов города', 'Отрасли компаний')


class Statistics(StatesGroup):
    name = State()
    region = State()

    texts = {
        'Statistics:name': 'Введите профессию заново',
        'Statistics:region': 'Введите регион заново',
    }


class Dictionary(StatesGroup):
    name = State()
    action = State()

    text = {
        'Dictionary:name': 'Введите необходимый справочник',
        'Dictionary:action': 'Введите необходимое действие'
    }


@admin_router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет, над чем сегодня поработаем", reply_markup = ADMIN_KEYBOARD)


@admin_router.message(StateFilter('*'), Command('cancel'))
@admin_router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def cancel_handler(msg: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await msg.answer('Все действия отменены', reply_markup = ADMIN_KEYBOARD)


@admin_router.message(StateFilter('*'), Command('back'))
@admin_router.message(StateFilter('*'), F.text.casefold() == 'назад')
async def step_back_handler(msg: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == Statistics.name:
        await msg.answer('Предыдущего шага не предусмотрено. Введите название профессии или нажмите "отмена"')
        return

    previous = None
    for step in Statistics.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await msg.answer(f"Окей, вы вернулись к прошлому шагу \n{Statistics.texts[previous.state]}")
            return
        previous = step


# Статистика
@admin_router.message(StateFilter(None), F.text == "Просмотреть статистику")
async def start_stats_handler(msg: Message, state: FSMContext):
    await msg.answer("Гружу статы. Введи профессию", reply_markup = ADMIN_KEYBOARD)
    await state.set_state(Statistics.name)


# Запросы по справочным данным
@admin_router.message(StateFilter(None), F.text == "Выполнить запрос")
async def start_dictionary_handler(msg: Message, state: FSMContext):
    await msg.answer('Выбери название справочника', reply_markup = ADMIN_DICTIONARY_KEYBOARD)
    await state.set_state(Dictionary.name)

@admin_router.message(StateFilter(Dictionary.name), F.text)
async def dictionary_action_handler(msg: Message, state:FSMContext):
    name = F.text
    request_data = {
        'locale': 'RU',
        'host': 'hh.ru'
    }

    await get_areas(request_data)
    await msg.answer('Словарь получен')
