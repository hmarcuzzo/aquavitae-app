from typing import Optional

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.appointment.dto.appointment.appointment_dto import AppointmentDto
from src.modules.domain.appointment.dto.appointment.create_appointment_dto import (
    CreateAppointmentDto,
)
from src.modules.domain.appointment.dto.appointment.update_appointment_dto import (
    UpdateAppointmentDto,
)
from src.modules.domain.appointment.entities.appointment_entity import Appointment
from src.modules.domain.appointment.repositories.appointment_repository import AppointmentRepository


class AppointmentService:
    def __init__(self):
        self.appointment_repository = AppointmentRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_appointment(
        self, appointment_dto: CreateAppointmentDto, db: Session
    ) -> Optional[AppointmentDto]:

        new_appointment = await self.appointment_repository.create(appointment_dto, db)

        new_appointment = await self.appointment_repository.save(new_appointment, db)
        return AppointmentDto(**new_appointment.__dict__)

    async def get_all_appointments(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[AppointmentDto]]:
        pagination["relations"] = ["user"]

        [all_appointment, total] = await self.appointment_repository.find_and_count(
            pagination,
            db,
        )

        return create_pagination_response_dto(
            [AppointmentDto(**appointment.__dict__) for appointment in all_appointment],
            total,
            pagination["skip"],
            pagination["take"],
        )

    async def get_appointment_by_id(
        self, appointment_id: str, db: Session
    ) -> Optional[AppointmentDto]:
        appointment = await self.appointment_repository.find_one_or_fail(
            {
                "where": Appointment.id == appointment_id,
            },
            db,
        )

        return AppointmentDto(**appointment.__dict__)

    async def update_appointment(
        self,
        appointment_id: str,
        update_appointment_dto: UpdateAppointmentDto,
        db: Session,
    ) -> Optional[UpdateResult]:
        return await self.appointment_repository.update(
            {"where": Appointment.id == appointment_id},
            update_appointment_dto,
            db,
        )

    async def delete_appointment(self, appointment_id: str, db: Session) -> Optional[UpdateResult]:
        return await self.appointment_repository.soft_delete(appointment_id, db)
