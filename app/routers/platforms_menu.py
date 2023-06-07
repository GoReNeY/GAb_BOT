from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from app.states.platforms_states import Platforms_Menu
from app.services.Database_API import DatabaseAPI
from app.settings import settings

platforms_menu_router = Router()


class Platforms_Menu_Router:

    @staticmethod
    @platforms_menu_router.message(Command("platforms"), State(None))
    async def platforms_menu(message: Message, state: FSMContext) -> None:

        async with DatabaseAPI() as api:
            platforms_dict = await api.get_user_platforms(message.from_user.id)  # type: ignore
            if platforms_dict.get("Access Denied"):
                return

        if platforms_dict.get("not_in_db"):
            platforms_dict = {key: False for key in settings.PLATFORMS}

        buttons_list = []

        for platform, status in platforms_dict.items():

            if status:
                buttons_list.append(InlineKeyboardButton(text=f"{platform} ✅".upper(), callback_data=f"{platform}"))
            else:
                buttons_list.append(InlineKeyboardButton(text=f"{platform} ❌".upper(), callback_data=f"{platform}"))

        keyboard_builder = InlineKeyboardBuilder()
        keyboard_builder.row(*buttons_list, width=2)
        keyboard_builder.row(InlineKeyboardButton(text="Вийти", callback_data='leave'))

        output_message = "Оберіть цікаві вам категорії:\n"

        await message.answer(output_message, reply_markup=keyboard_builder.as_markup())

        await state.set_data(platforms_dict)
        await state.set_state(Platforms_Menu.platforms_choosing)

    @staticmethod
    @platforms_menu_router.callback_query(Platforms_Menu.platforms_choosing)
    async def platforms_menu_processing(query: CallbackQuery, state: FSMContext) -> None:

        platforms_dict = await state.get_data()

        if query.data == 'leave':

            async with DatabaseAPI() as api:
                await api.set_user_platforms(query.from_user.id, platforms_dict)  # type: ignore

            await query.message.answer("Редагування категорій закінчено.")   # type: ignore
            await query.message.delete()   # type: ignore
            await query.answer()
            await state.clear()
            return

        if platforms_dict[query.data]:  # type: ignore
            platforms_dict[query.data] = False  # type: ignore
        else:
            platforms_dict[query.data] = True  # type: ignore

        buttons_list = []

        for platform, status in platforms_dict.items():

            if status:
                buttons_list.append(InlineKeyboardButton(text=f"{platform} ✅".upper(), callback_data=f"{platform}"))
            else:
                buttons_list.append(InlineKeyboardButton(text=f"{platform} ❌".upper(), callback_data=f"{platform}"))

        await state.update_data(platforms_dict)

        keyboard_builder = InlineKeyboardBuilder()
        keyboard_builder.row(*buttons_list, width=2)
        keyboard_builder.row(InlineKeyboardButton(text="Вийти", callback_data='leave'))

        output_message = "Оберіть цікаві вам категорії:\n"

        await query.message.edit_text(output_message, reply_markup=keyboard_builder.as_markup())  # type: ignore

        await query.answer()
