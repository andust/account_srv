from typing import Callable
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    DATABASE_PG_URL: PostgresDsn
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    WEB_APP_DEBUG: bool
    API_VERSION: str


@lru_cache()
def _configure_initial_settings() -> Callable[[], Settings]:
    load_dotenv()
    settings = Settings()

    def fn() -> Settings:
        return settings

    return fn


get_settings = _configure_initial_settings()
