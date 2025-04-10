from httpx import AsyncClient

from app.core.custom_logger import get_logger

logger = get_logger(__name__)


async def test_get_all_tables(aclient: AsyncClient):
    """Тестирование получения списка всех столиков"""
    logger.info("Тестирование получения списка всех столиков (эндпоинт /tables/)")
    response = await aclient.get("/tables/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    logger.info("✅ Тестирование получения списка всех столиков успешно пройдено")


async def test_create_new_table(aclient: AsyncClient):
    """Тестирование создания нового столика"""
    logger.info("Тестирование создания нового столика")
    response = await aclient.post(
        "/tables/",
        json={
            "name": "Table 11",
            "seats": 4,
            "location": "Столик у бара"
        }
    )
    assert response.status_code == 200
    assert response.json()["message"] == 'Стол с именем Table 11 успешно создан'
    logger.info("✅ Тестирование создания нового столика успешно пройдено")


async def test_create_new_table_invalid_data(aclient: AsyncClient):
    logger.info("Тестирование создания нового столика с некорректными данными")
    response = await aclient.post(
        "/tables/",
        json={
            "name": "Table 11",
            "seats": "invalid_seats",
            "location": "Столик у бара"
        }
    )
    assert response.status_code == 422
    logger.info("✅ Тестирование создания нового столика с некорректными данными успешно пройдено")


async def test_delete_table(aclient: AsyncClient):
    """Тестирование удаления столика"""
    logger.info("Тестирование удаления столика")
    table_id = 1
    response = await aclient.delete(f"/tables/{table_id}")
    assert response.status_code == 200
    assert response.json()["message"] == f'Стол с id = {table_id} успешно удален'
    logger.info("✅ Тестирование удаления столика успешно пройдено")


async def test_delete_table_invalid_id(aclient: AsyncClient):
    """Тестирование удаления столика с несуществующим id"""
    logger.info("Тестирование удаления столика с несуществующим id")
    table_id = 999999
    response = await aclient.delete(f"/tables/{table_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Стол с id = {table_id} не найден"

    table_id = -1
    response = await aclient.delete(f"/tables/{table_id}")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be greater than 0"
    logger.info("✅ Тестирование удаления столика с несуществующим id успешно пройдено")

