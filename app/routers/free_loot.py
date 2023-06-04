from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from app.services.Games_API import GamesAPI
from app.services.Database_API import DatabaseAPI
from app.services.Utils_API import UtilsAPI

from app.states.loot_states import Loot_States

from app.messages.game_messages import GAME_MESSAGE, GAME_MESSAGE_WITHOUT_DESCRIPTION

from app.models.game import Game

free_loot_router = Router()


@free_loot_router.message(Command("loot"), State(None))
async def loot(message: Message, state: FSMContext) -> None:

    async with DatabaseAPI() as api:
        platforms_dict = await api.get_user_platforms(message.from_user.id)  # type: ignore
        if platforms_dict.get("Access Denied"):
            return

    async with GamesAPI() as api:
        platforms_list = ".".join(filter(lambda key: platforms_dict[key], platforms_dict.keys()))
        raw_loot: list[dict] | None = await api.get_free_games_by_platforms(platforms_list, type="loot")

    if not raw_loot:
        await message.answer("Нажаль на даний момент роздач луту по вашим категоріям немає.")
        return

    loot_to_show: list[Game] = list(map(lambda game: Game.parse_obj(game), raw_loot))

    loot = loot_to_show[0]

    async with UtilsAPI() as api:
        loot.description = await api.translate(loot.description)
        loot.price = await api.convert(loot.price)

    loot_message = GAME_MESSAGE.format(loot.open_giveaway,
                                       loot.title,
                                       loot.description,
                                       loot.price,
                                       loot.published_date,
                                       loot.end_date,
                                       loot.platforms)

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(InlineKeyboardButton(text="⬅️", callback_data="prev"),
                         InlineKeyboardButton(text="➡️", callback_data="next"), width=2)

    keyboard_builder.row(InlineKeyboardButton(text="Вийти", callback_data='leave'))

    await message.answer_photo(loot.image, loot_message, reply_markup=keyboard_builder.as_markup())

    await state.set_state(Loot_States.watching_free_loot)
    await state.update_data(loot=loot_to_show, position=0)


@free_loot_router.callback_query(Loot_States.watching_free_loot)
async def showing_loot(query: CallbackQuery, state: FSMContext) -> None:

    if query.data == "leave":
        await query.message.answer("Перегляд луту закінчено.")   # type: ignore
        await query.message.delete()   # type: ignore
        await query.answer()
        await state.clear()
        return

    loot_to_show = (await state.get_data())['loot']
    position = (await state.get_data())['position']

    if len(loot_to_show) == 1:
        await query.answer()
        return

    match query.data:
        case "prev":
            position -= 1

            if position == -1:
                position = len(loot_to_show)-1

            loot: Game = loot_to_show[position]

        case "next":
            position += 1

            if position > len(loot_to_show)-1:
                position = 0

            loot: Game = loot_to_show[position]

        case _:
            return

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(InlineKeyboardButton(text="⬅️", callback_data="prev"),
                         InlineKeyboardButton(text="➡️", callback_data="next"), width=2)

    keyboard_builder.row(InlineKeyboardButton(text="Вийти", callback_data='leave'))

    async with UtilsAPI() as api:
        loot.description = await api.translate(loot.description)
        loot.price = await api.convert(loot.price)

    loot_message = GAME_MESSAGE.format(loot.open_giveaway,
                                       loot.title,
                                       loot.description,
                                       loot.price,
                                       loot.published_date,
                                       loot.end_date,
                                       loot.platforms)

    if len(loot_message) >= 1000:
        loot_message = GAME_MESSAGE_WITHOUT_DESCRIPTION.format(loot.open_giveaway,
                                                               loot.title,
                                                               loot.gamerpower_url,
                                                               loot.price,
                                                               loot.published_date,
                                                               loot.end_date,
                                                               loot.platforms)

    await query.message.edit_media(InputMediaPhoto(media=loot.image))  # type: ignore
    await query.message.edit_caption(caption=loot_message,  # type: ignore
                                     reply_markup=keyboard_builder.as_markup())

    await state.update_data(position=position)
