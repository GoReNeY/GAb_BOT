from app.services.Base_API import BaseAPI
from app.settings import settings

from typing import List


class GamesAPI(BaseAPI):

    _base_url = settings.API_URL

    async def get_all_free_games(self) -> List[dict] | None:
        async with self._session.get("/free_games/all") as responce:
            return await responce.json()

    async def get_free_games_by_platforms(self, platform, type="game") -> List[dict] | None:
        async with self._session.get("/free_games/giveaway_p", params={"platform": platform, "type": type}) as responce:
            return await responce.json()
