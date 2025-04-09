from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.custom_logger import get_logger
from app.models.table import TableORM
from app.schemas.tables_sch import TableRead, TableCreate

logger = get_logger(__name__)


class TableRepo:
    @classmethod
    async def get_tables(cls, session: AsyncSession) -> list[TableRead]:
        """Получить список всех столов"""
        logger.info("Получение списка всех столов")
        query = select(TableORM)
        tables_model = await session.execute(query)
        logger.info("Список всех столов получен")
        tables_model = tables_model.scalars().all()
        tables_list = [TableRead.model_validate(table) for table in tables_model]
        return tables_list

    @classmethod
    async def create_table(cls, new_table: TableCreate, session: AsyncSession) -> str:
        """Создать новый стол"""
        logger.info("Создание нового стола c именем {}".format(new_table.name))
        table = TableORM(**new_table.model_dump())
        session.add(table)
        await session.commit()
        message = "Стол с именем {} успешно создан".format(new_table.name)
        logger.info(message)
        return message

    @classmethod
    async def delete_table(cls, table_id: int, session: AsyncSession) -> str:
        """Удалить стол по id"""
        logger.info(f"Удаление стола по id = {table_id}")
        query = select(TableORM).where(TableORM.id == table_id)
        result = await session.execute(query)
        table_model = result.scalars().first()
        if table_model is None:
            message = "Стол с id = {} не найден".format(table_id)
            logger.info(message)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

        # Удаляем стол из базы данных
        delete_query = delete(TableORM).where(TableORM.id == table_id)
        await session.execute(delete_query)
        await session.commit()
        message = "Стол с id = {} успешно удален".format(table_id)
        logger.info(message)
        return message
