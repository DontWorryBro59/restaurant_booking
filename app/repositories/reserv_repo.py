from datetime import timedelta, datetime

from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.custom_logger import get_logger
from app.models.reservation import ReservationORM
from app.repositories.tables_repo import TableRepo
from app.schemas.reservations_sch import ReservationRead, ReservationCreate

logger = get_logger(__name__)


class ReservRepo:
    @classmethod
    async def get_reservations(cls, session: AsyncSession) -> list[ReservationRead]:
        """Получить список всех столов"""
        logger.info("Получение списка всех столов")
        query = select(ReservationORM)
        reservation_models = await session.execute(query)
        logger.info("Список всех столов получен")
        reservation_models = reservation_models.scalars().all()
        reservations_list = [ReservationRead.model_validate(reservation) for reservation in reservation_models]
        return reservations_list

    @classmethod
    async def create_reservation(cls, new_reservation: ReservationCreate, session: AsyncSession) -> str:
        """Создать новое бронирование"""
        logger.info("Создание нового бронирования")
        # Проверяем наличие конфликта бронирования в базе данных
        conflict = await cls.check_reservation_conflict(session=session,
                                                        table_id=new_reservation.table_id,
                                                        reservation_time=new_reservation.reservation_time,
                                                        duration_minutes=new_reservation.duration_minutes)
        if conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Бронирование пересекается с существующим бронированием"
            )
        # Создаем новое бронирование и сохраняем его в базе данных
        new_reservation = ReservationORM(**new_reservation.model_dump())
        session.add(new_reservation)
        await session.commit()

        message = "Бронирование успешно создано"
        return message

    @classmethod
    async def delete_reservation(cls, reservation_id: int, session: AsyncSession) -> str:
        """Удалить бронирование по id"""
        logger.info("Удаление бронирования по id={}".format(reservation_id))
        # Получаем бронирование по указанному id
        query = select(ReservationORM).where(ReservationORM.id == reservation_id)
        result = await session.execute(query)
        reservation_model = result.scalars().first()
        if reservation_model is None:
            message = "Бронирование с id = {} не найдено".format(reservation_id)
            logger.info(message)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

        # Удаляем бронирование из базы данных
        delete_query = delete(ReservationORM).where(ReservationORM.id == reservation_id)
        await session.execute(delete_query)
        await session.commit()
        message = "Бронирование с id = {} успешно удалено".format(reservation_id)
        logger.info(message)
        return message

    @classmethod
    async def check_reservation_conflict(cls, session, table_id: int, reservation_time: datetime,
                                         duration_minutes: int) -> bool:
        new_start = reservation_time
        new_end = reservation_time + timedelta(minutes=duration_minutes)

        # Проверяем есть ли указанный стол в базе данных
        table = await TableRepo.get_table_by_id(session=session, table_id=table_id)
        if not table:
            message = "Стол с именем {} не найден".format(table_id)
            logger.info(message)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

        # Получаем все брони по указанному столику
        query = select(ReservationORM).where(
            ReservationORM.table_id == table_id
        )
        result = await session.execute(query)
        reservations = result.scalars().all()

        for existing in reservations:
            existing_start = existing.reservation_time
            existing_end = existing_start + timedelta(minutes=existing.duration_minutes)

            # Проверка пересечения интервалов
            if existing_start < new_end and existing_end > new_start:
                return True

        return False
