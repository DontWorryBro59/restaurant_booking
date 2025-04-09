from fastapi import APIRouter, Depends

from app.database.database_helper import db_helper
from app.repositories.reserv_repo import ReservRepo
from app.schemas.additional_sch import MessageSchema
from app.schemas.reservations_sch import ReservationCreate, ReservationRead

reservation_router = APIRouter(tags=["📅 reservations"], prefix="/reservations")


@reservation_router.get('/')
async def get_all_reservations(session=Depends(db_helper.get_session)) -> list[ReservationRead]:
    """Запрос на получение списка всех бронирований"""
    reservations_list = await ReservRepo.get_reservations(session=session)
    return reservations_list


@reservation_router.post('/')
async def create_new_reservation(new_reservation: ReservationCreate,
                                 session=Depends(db_helper.get_session)) -> MessageSchema:
    """Создание нового бронирования"""
    message = await ReservRepo.create_reservation(new_reservation=new_reservation, session=session)
    return MessageSchema(message=message)


@reservation_router.delete('/{id}')
async def delete_reservation(id: int, session=Depends(db_helper.get_session)) -> MessageSchema:
    """Удаление существующего бронирование"""
    message = await ReservRepo.delete_reservation(reservation_id=id, session=session)
    return MessageSchema(message=message)
