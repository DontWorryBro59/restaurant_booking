from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

from app.core.config import settings
from app.core.custom_logger import get_logger
from app.models.base_models import Base

logger = get_logger(__name__)

# добавлена логика проверки режима работы приложения
# для использования разных баз данных в разных режимах работы

if settings.MODE == "TEST":
    DATABASE_URL = settings.get_db_url_test
    logger.info("Используется тестовая база данных")
elif settings.MODE in ["DEV", "PROD"]:
    DATABASE_URL = settings.get_db_url
    logger.warning("Внимание! Используется 'боевая' база данных")
else:
    raise ValueError("Неверное значение переменной окружения 'MODE'")

# Создаем асинхронный движок
async_engine = create_async_engine(DATABASE_URL, echo=settings.DB_ECHO)

# Сессия для асинхронных запросов
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


class DBHelper:
    def __init__(self, engine: AsyncEngine, async_session: AsyncSession):
        self.async_engine = engine
        self.async_session_maker = async_session

    # Вспомогательные методы для работы с базой данных
    async def _create_all(self) -> None:
        """Создание всех таблиц в базе данных"""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Таблицы в базе данных созданы")

    async def _drop_all(self) -> None:
        """Удаление всех таблиц из базы данных"""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("Таблицы в базе данных удалены")

    # Генератор асинхронной сессии для работы с базой данных (инъекции)
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Получение асинхронной сессии для работы с базой данных"""
        async with self.async_session_maker() as session:
            logger.info("Сессия базы данных получена")
            yield session


db_helper = DBHelper(async_engine, AsyncSessionLocal)
