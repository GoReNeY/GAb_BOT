from pydantic import BaseSettings, SecretStr, AnyUrl


class Settings(BaseSettings):

    BOT_TOKEN: SecretStr
    API_URL: AnyUrl

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore
