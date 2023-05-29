from app.services.Base_API import BaseAPI
from app.settings import settings
from app.models.game import Game

from typing import List, Dict


class GAbAPI(BaseAPI):

    _base_url = settings.API_URL

    async def get_all_free_games(self) -> List[Game]:
        async with self._session.get("/free_games/all") as responce:
            return await responce.json()

    async def get_free_games_by_platform(self, platform) -> List[Game]:
        async with self._session.get("/free_games/giveaway_p", params={"platform": platform}) as responce:
            return await responce.json()

    @staticmethod
    def get_headers() -> Dict[str, str]:
        return {}
