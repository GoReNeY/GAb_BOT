from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from app.states.categories_states import Categories_Menu
from app.settings import settings

categories_menu_router = Router()


@categories_menu_router.message(Command("categories"))
async def categories_menu(message: Message, state: FSMContext) -> None:

    # get запрос к апи с проверкой на наличие в БД данных о юзере

    categories_dict = {key: False for key in settings.PLATFORMS}
    buttons_list = []

    output_message = "Оберіть цікаві вам категорії:\n"

    for platform, status in categories_dict.items():

        buttons_list.append(InlineKeyboardButton(text=f"{platform}".upper(), callback_data=f"{platform}"))

        if status:
            output_message += f"\n{platform}".upper() + "\t\t✅"
        else:
            output_message += f"\n{platform}".upper() + "\t\t❌"

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(*buttons_list, width=2)
    keyboard_builder.row(InlineKeyboardButton(text="Вийти", callback_data='deny'))

    await message.answer(output_message, reply_markup=keyboard_builder.as_markup())

    await state.set_data(categories_dict)
    await state.set_state(Categories_Menu.categories_choosing)


@categories_menu_router.callback_query(Categories_Menu.categories_choosing)
async def categories_menu_processing(query: CallbackQuery, state: FSMContext) -> None:

    categories_dict = await state.get_data()

    if categories_dict[query.data]:  # type: ignore
        categories_dict[query.data] = False  # type: ignore
    else:
        categories_dict[query.data] = True  # type: ignore

    buttons_list = []
    output_message = "Оберіть цікаві вам категорії:\n"

    for platform, status in categories_dict.items():

        buttons_list.append(InlineKeyboardButton(text=f"{platform}".upper(), callback_data=f"{platform}"))

        if status:
            output_message += f"\n{platform}".upper() + "\t\t✅"
        else:
            output_message += f"\n{platform}".upper() + "\t\t❌"

    await state.update_data(categories_dict)

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(*buttons_list, width=2)
    keyboard_builder.row(InlineKeyboardButton(text="Вийти", callback_data='deny'))

    await query.message.edit_text(output_message, reply_markup=keyboard_builder.as_markup())  # type: ignore

    await query.answer()
