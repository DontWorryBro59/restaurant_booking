from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.core.custom_logger import get_logger
from app.database.database_helper import db_helper
from app.routers.reserv_router import reservation_router
from app.routers.tables_router import tables_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Приложение запускается")
    # Выполняем дополнительные действия в зависимости от режима работы
    await check_app_mode()
    yield
    logger.info("🛑 Приложение останавливается")


async def check_app_mode():
    if settings.MODE == "DEV":
        logger.info("💻💻💻💻 Приложение находится в режиме разработки 💻💻💻💻")
        logger.info("Запущен процесс очистки и создания таблиц")
        logger.info("Удаляем все таблицы в базе данных")
        await db_helper._drop_all()
        logger.info("Создаем все таблицы в базе данных")
        await db_helper._create_all()


app = FastAPI(lifespan=lifespan)

# Добавляем роутеры
app.include_router(tables_router)
app.include_router(reservation_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
