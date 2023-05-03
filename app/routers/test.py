from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

test_router = Router()


@test_router.message(Command("test"))  # [2]
async def test(message: Message):
    await message.answer("тест")
