from aiogram import types, Router, F
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup

from src.bot import configs
from src.apies.main import create_data_collector
from src.bot.filters.chat_types import ChatTypeFilter, IsAdmin
from src.bot.keyboards.reply import get_keyboard
from src.bot.response_optimizer import optimization_result

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())
data_collector = create_data_collector()

ADMIN_KEYBOARD = get_keyboard('Просмотреть статистику', 'Войти как пользователь', 'Удалить')


class Statistics(StatesGroup):
    name = State()
    region = State()

    texts = {
        'Statistics:name': 'Введите профессию заново',
        'Statistics:region': 'Введите регион заново',
    }


@admin_router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет, над чем сегодня поработаем", reply_markup = ADMIN_KEYBOARD)


@admin_router.message(StateFilter(None), F.text == "Просмотреть статистику")
async def start_handler(msg: Message, state: FSMContext):
    await msg.answer("Гружу статы. Введи профессию", reply_markup = ADMIN_KEYBOARD)
    await state.set_state(Statistics.name)


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

@admin_router.message(Statistics.name, F.text)
async def add_proffesion(msg: Message, state: FSMContext):
    if len(msg.text) > 100:
        await msg.answer(f'Слишком длинная профессия.\nВведите заново')
        return

    await state.update_data(name = msg.text)
    await msg.answer('Введите регион')
    await state.set_state(Statistics.region)


@admin_router.message(Statistics.region, F.text)
async def add_region(msg: Message, state: FSMContext):
    if len(msg.text) > 100:
        await msg.answer(f'Слишком длинное название для региона.\nВведите заново')
        return

    await state.update_data(region = msg.text)
    data = await state.get_data()
    await msg.answer(str(data))
    await state.clear()


@admin_router.message(F.text == "Войти как пользователь")
async def start_handler(msg: Message):
    await msg.answer("Теперь ты обычный юзер", reply_markup = ADMIN_KEYBOARD)
