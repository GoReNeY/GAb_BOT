from aiogram import Router
from aiogram.filters import Text, Command
from aiogram import types
from aiogram.fsm.context import FSMContext

from app.messages.start_message import START_MESSAGE

utils_router = Router()


@utils_router.message(Command("deny"))
@utils_router.callback_query(Text('deny'))
async def deny_fsm(callback: types.CallbackQuery | types.Message, state: FSMContext) -> None:

    match type(callback):

        case types.CallbackQuery:
            query: types.CallbackQuery = callback  # type: ignore

            await query.message.answer("Діалог закінчено.")  # type: ignore
            await query.message.delete()  # type: ignore
            await query.answer()

        case types.Message:
            message: types.CallbackQuery = callback  # type: ignore

            await message.answer("Всі діалоги закінчено.")  # type: ignore
            await message.delete()  # type: ignore

    await state.clear()


@utils_router.message(Command("start"))
async def start(message: types.Message, state: FSMContext) -> None:
    await message.answer(START_MESSAGE)  # type: ignore
