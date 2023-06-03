from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from app.services.Games_API import GamesAPI
from app.services.Database_API import DatabaseAPI

from app.states.games_states import Games_States

from app.messages.game_messages import GAME_MESSAGE, GAME_MESSAGE_WITHOUT_DESCRIPTION

from app.models.game import Game

free_games_router = Router()


@free_games_router.message(Command("games"))
async def games(message: Message, state: FSMContext) -> None:

    async with DatabaseAPI() as api:
        platforms_dict = await api.get_user_platforms(message.from_user.id)  # type: ignore
        if platforms_dict.get("Access Denied"):
            return

    async with GamesAPI() as api:
        platforms_list = ".".join(filter(lambda key: platforms_dict[key], platforms_dict.keys()))
        raw_games: list[dict] | None = await api.get_free_games_by_platforms(platforms_list, type="game")

    if not raw_games:
        await message.answer("Нажаль на даний момент роздач ігор по вашим категоріям немає.")
        return

    games_to_show: list[Game] = list(map(lambda game: Game.parse_obj(game), raw_games))

    game = games_to_show[0]
    game_message = GAME_MESSAGE.format(game.open_giveaway,
                                       game.title,
                                       game.description,
                                       game.price,
                                       game.published_date,
                                       game.end_date,
                                       game.platforms)

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(InlineKeyboardButton(text="⬅️", callback_data="prev"),
                         InlineKeyboardButton(text="➡️", callback_data="next"), width=2)

    keyboard_builder.row(InlineKeyboardButton(text="Вийти", callback_data='leave'))

    await message.answer_photo(game.image, game_message, reply_markup=keyboard_builder.as_markup())

    await state.set_state(Games_States.watching_free_games)
    await state.update_data(games=games_to_show, position=0)


@free_games_router.callback_query(Games_States.watching_free_games)
async def showing_games(query: CallbackQuery, state: FSMContext) -> None:

    if query.data == "leave":
        await query.message.answer("Перегляд ігор закінчено.")   # type: ignore
        await query.message.delete()   # type: ignore
        await query.answer()
        await state.clear()
        return

    games_to_show = (await state.get_data())['games']
    position = (await state.get_data())['position']

    if len(games_to_show) == 1:
        await query.answer()
        return

    match query.data:
        case "prev":
            position -= 1

            if position == -1:
                position = len(games_to_show)-1

            game: Game = games_to_show[position]

        case "next":
            position += 1

            if position > len(games_to_show)-1:
                position = 0

            game: Game = games_to_show[position]

        case _:
            return

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(InlineKeyboardButton(text="⬅️", callback_data="prev"),
                         InlineKeyboardButton(text="➡️", callback_data="next"), width=2)

    keyboard_builder.row(InlineKeyboardButton(text="Вийти", callback_data='leave'))

    game_message = GAME_MESSAGE.format(game.open_giveaway,
                                       game.title,
                                       game.description,
                                       game.price,
                                       game.published_date,
                                       game.end_date,
                                       game.platforms)

    if len(game_message) >= 1000:
        game_message = GAME_MESSAGE_WITHOUT_DESCRIPTION.format(game.open_giveaway,
                                                               game.title,
                                                               game.gamerpower_url,
                                                               game.price,
                                                               game.published_date,
                                                               game.end_date,
                                                               game.platforms)

    await query.message.edit_media(InputMediaPhoto(media=game.image))  # type: ignore
    await query.message.edit_caption(caption=game_message,  # type: ignore
                                     reply_markup=keyboard_builder.as_markup())

    await state.update_data(position=position)
