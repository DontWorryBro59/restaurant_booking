import json
from datetime import datetime, timedelta, UTC

import pytest
from fastapi import HTTPException

from app.core.custom_logger import get_logger
from app.repositories.reserv_repo import ReservRepo
from app.schemas.reservations_sch import ReservationCreate

logger = get_logger(__name__)


def get_mock_data(model: str) -> list[dict]:
    with open(f"app/tests/mock_data/mock_{model}.json", "r", encoding="utf-8") as file:
        raw_data = json.load(file)
    return raw_data


def get_time_now() -> datetime:
    utc_now = datetime.now(UTC)
    new_time = utc_now + timedelta(hours=1)
    return new_time


async def test_get_reservations(session):
    """Тестирование получения списка всех резервирований"""
    logger.info("Тестирование получения списка всех резервирований")
    reservations = await ReservRepo.get_reservations(session=session)
    assert len(reservations) == 0
    logger.info("✅ Тестирование получения списка всех резервирований успешно пройдено")


async def test_create_reservation(session):
    """Тестирование создания нового резервирования"""
    logger.info("Тестирование создания нового резервирования")
    new_reservation = ReservationCreate(
        customer_name="John Doe",
        table_id=1,
        reservation_time=get_time_now(),
        duration_minutes=60,
    )
    message = await ReservRepo.create_reservation(
        new_reservation=new_reservation, session=session
    )
    assert message == "Бронирование успешно создано"
    logger.info("✅ Тестирование создания нового резервирования успешно пройдено")
    reservations = await ReservRepo.get_reservations(session=session)
    assert len(reservations) == 1
    logger.info("✅ Тестирование получения списка всех резервирований успешно пройдено")


async def test_create_reservation_conflict(session):
    logger.info("Тестирование создания нового резервирования")
    new_reservation = ReservationCreate(
        customer_name="John Doe",
        table_id=1,
        reservation_time=get_time_now(),
        duration_minutes=60,
    )
    conflict_reservation = ReservationCreate(
        customer_name="Jane Doe",
        table_id=1,
        reservation_time=get_time_now(),
        duration_minutes=60,
    )
    message = await ReservRepo.create_reservation(
        new_reservation=new_reservation, session=session
    )
    assert message == "Бронирование успешно создано"
    with pytest.raises(HTTPException) as exc_info:
        message = await ReservRepo.create_reservation(
            new_reservation=conflict_reservation, session=session
        )
    assert exc_info.value.status_code == 400
    assert (
        exc_info.value.detail
        == "Бронирование пересекается с существующим бронированием"
    )


async def test_delete_reservation(session):
    logger.info("Тестирование удаления резервирования")
    new_reservation = ReservationCreate(
        customer_name="John Doe",
        table_id=1,
        reservation_time=get_time_now(),
        duration_minutes=60,
    )
    message = await ReservRepo.create_reservation(
        new_reservation=new_reservation, session=session
    )
    reservation_id = 1
    message = await ReservRepo.delete_reservation(
        reservation_id=reservation_id, session=session
    )
    reservations = await ReservRepo.get_reservations(session=session)
    assert len(reservations) == 0
    logger.info("✅ Тестирование удаления резервирования успешно пройдено")
