from app.services.Base_API import BaseAPI
from app.settings import settings


class UtilsAPI(BaseAPI):

    _base_url = settings.API_URL

    async def translate(self, text: str) -> str:
        async with self._session.post("/utils/translate", data=text) as responce:
            return await responce.json()

    async def convert(self, cost: str) -> str:

        async with self._session.post("/utils/convert", data=cost) as responce:
            return await responce.json()
