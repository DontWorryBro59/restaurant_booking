from fastapi import APIRouter

from app.schemas.tables_sch import TableCreate

tables_router = APIRouter(tags=["🍽️ tables"], prefix="/tables")

@tables_router.get('/')
async def get_all_tables():
    """Return list of tables"""
    pass

@tables_router.post('/')
async def create_new_table(new_table: TableCreate):
    """Create a new table"""
    pass

@tables_router.delete('/{id}')
async def delete_table(id: int):
    """Delete table"""
    pass

