import json

from app.services.Base_API import BaseAPI
from app.settings import settings

from typing import Dict


class DatabaseAPI(BaseAPI):

    _base_url = settings.API_URL

    async def get_user_platforms(self, user_id: int) -> Dict[str, bool]:
        async with self._session.get("/database/platforms", params={'user_id': user_id}) as responce:
            return await responce.json()

    async def set_user_platforms(self, user_id: int, data: dict) -> Dict[str, bool]:

        platforms = json.dumps(data)

        async with self._session.put("/database/platforms", data=platforms, params={'user_id': user_id}) as responce:
            return await responce.json()
