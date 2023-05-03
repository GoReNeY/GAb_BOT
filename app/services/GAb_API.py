from app.services.Base_API import BaseAPI
from app.settings import settings
from app.models.game import Game

from typing import List, Dict


class GAbAPI(BaseAPI):

    _base_url = settings.API_URL

    async def get_current_epic_games(self) -> List[Game]:
        async with self._session.get("/epic_free_games/current") as responce:
            return await responce.json()

    async def get_next_epic_games(self) -> List[Game]:
        async with self._session.get("/epic_free_games/coming_soon") as responce:
            return await responce.json()

    @staticmethod
    def get_headers() -> Dict[str, str]:
        return {}
