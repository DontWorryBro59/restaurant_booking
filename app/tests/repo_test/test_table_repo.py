### Тестирование репозитория столов
import json
from datetime import datetime, timedelta, UTC

import pytest
from fastapi import HTTPException

from app.core.custom_logger import get_logger
from app.routers.tables_router import TableRepo
from app.schemas.tables_sch import TableCreate

logger = get_logger(__name__)


def get_mock_data(model: str) -> list[dict]:
    with open(
            f"app/tests/mock_data/mock_{model}.json", "r", encoding="utf-8"
    ) as file:
        raw_data = json.load(file)
    return raw_data


def get_time_now() -> datetime:
    utc_now = datetime.now(UTC)
    new_time = utc_now + timedelta(hours=1)
    return new_time


async def test_get_tables(session):
    """Тестирование получения списка всех столов"""
    logger.info("Тестирование получения списка всех столов")
    tables = await TableRepo.get_tables(session=session)
    assert len(tables) == len(get_mock_data("tables"))
    logger.info("✅ Тестирование получения списка всех столов успешно пройдено")


async def test_create_table(session):
    """Тестирование создания нового стола"""
    logger.info("Тестирование создания нового стола")
    new_table = TableCreate(**get_mock_data("tables")[0])
    message = await TableRepo.create_table(new_table=new_table, session=session)
    tables = await TableRepo.get_tables(session=session)
    assert len(tables) == len(get_mock_data("tables")) + 1
    logger.info("✅ Тестирование создания нового стола успешно пройдено")


async def test_delete_table(session):
    """Тестирование удаления стола по id"""
    logger.info("Тестирование удаления стола по id")
    table_id = 1
    message = await TableRepo.delete_table(table_id=table_id, session=session)
    tables = await TableRepo.get_tables(session=session)
    assert len(tables) == len(get_mock_data("tables")) - 1
    logger.info("✅ Тестирование удаления стола по id успешно пройдено")


async def test_delete_table_not_found(session):
    """Тестирование удаления стола по несуществующему id"""
    table_id = -1
    # Проверяем, что вызывается HTTPException с кодом 404
    with pytest.raises(HTTPException) as exc_info:
        await TableRepo.delete_table(table_id=table_id, session=session)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Стол с id = {table_id} не найден"
    logger.info("✅ Тестирование удаления стола по несуществующему id успешно пройдено")


async def test_get_table_by_id(session):
    """Тестирование получения стола по id"""
    logger.info("Тестирование получения стола по id")
    table_id = 1
    table = await TableRepo.get_table_by_id(table_id=table_id, session=session)
    assert table.name == "Table 1"
    assert table.id == table_id
    logger.info("✅ Тестирование получения стола по id успешно пройдено")


async def test_get_table_by_id_not_found(session):
    """Тестирование получения стола по несуществующему id"""
    logger.info("Тестирование получения стола по несуществующему id")
    table_id = -1
    with pytest.raises(HTTPException) as exc_info:
        await TableRepo.delete_table(table_id=table_id, session=session)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Стол с id = {table_id} не найден"
    logger.info("✅ Тестирование получения стола по несуществующему id успешно пройдено")
