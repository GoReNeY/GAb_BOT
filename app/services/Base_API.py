from typing import Dict
from pydantic import AnyUrl
from aiohttp import ClientSession

from app.settings import settings


class BaseAPI():

    _base_url: AnyUrl

    def __init__(self):
        self._session = ClientSession(self._base_url, headers=self.get_headers())

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def close(self) -> None:
        await self._session.close()

    @staticmethod
    def get_headers() -> Dict[str, str]:
        return {
            "Autorization": settings.BOT_TOKEN.get_secret_value()
        }
