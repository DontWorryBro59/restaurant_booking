from typing import Literal

from dotenv import load_dotenv
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Общие переменные окружения
    DB_ECHO: bool
    MODE: Literal["DEV", "PROD", "TEST"]

    # переменные окружения для базы данных
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_LOGIN: str
    DB_PASSWORD: str

    # переменные окружения для тестов
    DB_HOST_TEST: str
    DB_PORT_TEST: int
    DB_NAME_TEST: str
    DB_LOGIN_TEST: str
    DB_PASSWORD_TEST: str

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def get_db_url(self) -> str:
        """Возвращает строку подключения к базе данных"""
        return f"postgresql+asyncpg://{self.DB_LOGIN}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def get_db_url_test(self) -> str:
        """Возвращает строку подключения к базе данных для тестов"""
        return f"postgresql+asyncpg://{self.DB_LOGIN_TEST}:{self.DB_PASSWORD_TEST}@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}"


settings = Settings()
