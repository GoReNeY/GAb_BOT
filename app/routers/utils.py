from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

utils_router = Router()


@utils_router.callback_query(Text('deny'))
async def deny_fsm(query: CallbackQuery, state: FSMContext) -> None:

    await state.clear()

    await query.message.answer("Редагування категорій закінчено.")  # type: ignore
    await query.answer()
