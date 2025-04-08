from fastapi import APIRouter

from app.schemas.reservations_sch import ReservationCreate

reservation_router = APIRouter(tags=["📅 reservations"], prefix="/reservations")


@reservation_router.get('/')
async def get_all_reservations():
    """Return list of reservations"""
    pass


@reservation_router.post('/')
async def create_new_reservation(new_reservation: ReservationCreate):
    """Create a new reservation"""
    pass


@reservation_router.delete('/{id}')
async def delete_reservation(id: int):
    """Delete reservation"""
    pass
