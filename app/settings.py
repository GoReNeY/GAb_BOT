from pydantic import BaseSettings, SecretStr, AnyUrl


class Settings(BaseSettings):

    BOT_TOKEN: SecretStr
    API_URL: AnyUrl

    PLATFORMS: list[str] = ["pc", "steam", "epic-games-store", "ubisoft", "gog", "itchio", "ps4", "ps5", "xbox-one",
                            "xbox-series-xs", "switch", "android", "ios", "vr", "battlenet", "origin", "drm-free",
                            "xbox-360"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore
