from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenuCallback(CallbackData, prefix='menu'):
    level: int
    menu_name: str


def get_callback_btns(*, btns: dict[str, str], sizes: tuple[int] = (2, )):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


def get_user_main_btns(*, level: int, sizes: tuple[int] = (2, )):
    keyboard = InlineKeyboardBuilder()
    btns = {
        'Поиск': 'search',
        'Личный кабинет': 'user_area',
        'О нас': 'about'
    }

    for text, menu_name in btns.items():
        if menu_name == 'search':
            keyboard.add(InlineKeyboardButton(text = text,
                callback_data = MenuCallback(level=level+1, menu_name = menu_name).pack()))
        elif menu_name == 'user_area':
            keyboard.add(InlineKeyboardButton(text = text,
                callback_data = MenuCallback(level=level+1, menu_name = menu_name).pack()))
        else:
            keyboard.add(InlineKeyboardButton(text = text,
                callback_data = MenuCallback(level=level, menu_name = menu_name).pack()))
            
    return keyboard.adjust(*sizes).as_markup()