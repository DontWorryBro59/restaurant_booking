from fastapi import APIRouter, Depends, Path

from app.database.database_helper import db_helper
from app.repositories.tables_repo import TableRepo
from app.schemas.additional_sch import MessageSchema
from app.schemas.tables_sch import TableCreate, TableRead

tables_router = APIRouter(tags=["🍽️ tables"], prefix="/tables")


@tables_router.get('/')
async def get_all_tables(session=Depends(db_helper.get_session)) -> list[TableRead]:
    """Получаем список всех столов"""
    all_tables = await TableRepo.get_tables(session=session)
    return all_tables


@tables_router.post('/')
async def create_new_table(new_table: TableCreate, session=Depends(db_helper.get_session)) -> MessageSchema:
    message = await TableRepo.create_table(new_table=new_table, session=session)
    return MessageSchema(message=message)


@tables_router.delete('/{id}')
async def delete_table(id: int = Path(..., gt=0, description="ID стола, должен быть больше нуля"),
                       session=Depends(db_helper.get_session)) -> MessageSchema:
    """Удаляем стол по id"""
    message = await TableRepo.delete_table(table_id=id, session=session)
    return MessageSchema(message=message)
