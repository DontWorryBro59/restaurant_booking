from fastapi import APIRouter, Depends, Path

from app.core.custom_logger import get_logger
from app.database.database_helper import db_helper
from app.repositories.tables_repo import TableRepo
from app.schemas.additional_sch import MessageSchema
from app.schemas.tables_sch import TableCreate, TableRead

tables_router = APIRouter(tags=["🍽️ tables"], prefix="/tables")

logger = get_logger(__name__)


@tables_router.get('/')
async def get_all_tables(session=Depends(db_helper.get_session)) -> list[TableRead]:
    """Получаем список всех столов"""
    logger.info("Использование роутера для получения списка всех столов")
    all_tables = await TableRepo.get_tables(session=session)
    return all_tables


@tables_router.post('/')
async def create_new_table(new_table: TableCreate, session=Depends(db_helper.get_session)) -> MessageSchema:
    """Создаем новый стол"""
    logger.info("Использование роутера для создания нового стола")
    message = await TableRepo.create_table(new_table=new_table, session=session)
    return MessageSchema(message=message)


@tables_router.delete('/{table_id}')
async def delete_table(table_id: int = Path(..., gt=0, description="ID стола, должен быть больше нуля"),
                       session=Depends(db_helper.get_session)) -> MessageSchema:
    """Удаляем стол по id"""
    logger.info("Использование роутера для удаления стола по id")
    message = await TableRepo.delete_table(table_id=table_id, session=session)
    return MessageSchema(message=message)
