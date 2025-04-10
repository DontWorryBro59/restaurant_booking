from datetime import datetime, UTC, timedelta

from httpx import AsyncClient

from app.core.custom_logger import get_logger

logger = get_logger(__name__)


def get_time_now() -> datetime:
    utc_now = datetime.now(UTC)
    new_time = utc_now + timedelta(hours=1)
    return new_time


async def test_get_all_reservations(aclient: AsyncClient):
    """Тестирование получения списка всех бронирований"""
    logger.info(
        "Тестирование получения списка всех бронирований (эндпоинт /reservations/)"
    )
    response = await aclient.get("/reservations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    logger.info("✅ Тестирование получения списка всех бронирований успешно пройдено")


async def test_create_new_reservation(aclient: AsyncClient):
    """Тестирование создания нового бронирования"""
    logger.info("Тестирование создания нового бронирования")
    response = await aclient.post(
        "/reservations/",
        json={
            "customer_name": "Ivanov Ivan",
            "table_id": 1,
            "reservation_time": str(get_time_now()),
            "duration_minutes": 15,
        },
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Бронирование успешно создано"
    logger.info("✅ Тестирование создания нового бронирования успешно пройдено")


async def test_create_new_reservation_conflict(aclient: AsyncClient):
    """Тестирование создания нового бронирования с конфликтом времени"""
    logger.info("Тестирование создания нового бронирования с конфликтом времени")
    first_response = await aclient.post(
        "/reservations/",
        json={
            "customer_name": "Ivanov Ivan",
            "table_id": 1,
            "reservation_time": str(get_time_now()),
            "duration_minutes": 15,
        },
    )
    second_response = await aclient.post(
        "/reservations/",
        json={
            "customer_name": "Ivanov Ivan",
            "table_id": 1,
            "reservation_time": str(get_time_now()),
            "duration_minutes": 15,
        },
    )

    assert second_response.status_code == 400
    assert (
        second_response.json()["detail"]
        == "Бронирование пересекается с существующим бронированием"
    )


async def test_create_new_reservation_invalid_data(aclient: AsyncClient):
    """Тестирование создания нового бронирования с некорректными данными"""
    logger.info("Тестирование создания нового бронирования с некорректными данными")
    table_id = 9999
    response = await aclient.post(
        "/reservations/",
        json={
            "customer_name": "Ivanov Ivan",
            "table_id": table_id,
            "reservation_time": str(get_time_now()),
            "duration_minutes": 15,
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == f"Стол с id = {table_id} не найден"
    logger.info(
        "✅ Тестирование создания нового бронирования с некорректными данными успешно пройдено"
    )


async def test_delete_reservation(aclient: AsyncClient):
    """Тестирование удаления бронирования"""
    logger.info("Создание бронирования для удаления")
    response = await aclient.post(
        "/reservations/",
        json={
            "customer_name": "string",
            "table_id": 1,
            "reservation_time": str(get_time_now()),
            "duration_minutes": 15,
        },
    )

    logger.info("Тестирование удаления бронирования")
    reservation_id = 1
    response = await aclient.delete(f"/reservations/{reservation_id}")
    assert response.status_code == 200
    assert (
        response.json()["message"]
        == f"Бронирование с id = {reservation_id} успешно удалено"
    )
    logger.info("✅ Тестирование удаления бронирования успешно пройдено")


async def test_delete_reservation_not_found(aclient: AsyncClient):
    """Тестирование удаления несуществующего бронирования"""
    logger.info("Тестирование удаления несуществующего бронирования")
    reserv_id = 9999
    response = await aclient.delete(f"/reservations/{reserv_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Бронирование с id = {reserv_id} не найдено"
    logger.info(
        "✅ Тестирование удаления несуществующего бронирования успешно пройдено"
    )
