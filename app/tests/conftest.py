import asyncio
import json
from datetime import datetime

import pytest
import pytest_asyncio
from sqlalchemy import insert

from app.core.config import settings
from app.core.custom_logger import get_logger
from app.database.database_helper import db_helper
from app.models.reservation import ReservationORM  # noqa
from app.models.table import TableORM  # noqa

logger = get_logger(__name__)


@pytest_asyncio.fixture(autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"
    await db_helper._drop_all()
    logger.info("Dropping tasting database tables")
    await db_helper._create_all()
    logger.info("Creating tasting database tables")

    def open_mock_json(model: str):
        with open(
            f"app/tests/mock_data/mock_{model}.json", "r", encoding="utf-8"
        ) as file:
            raw_data = json.load(file)
        return raw_data

    tables = open_mock_json("tables")

    async with db_helper.async_session_maker() as session:
        add_tasks = insert(TableORM).values(tables)
        await session.execute(add_tasks)
        await session.commit()
        logger.info("Adding mock data to testing database")


# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()
