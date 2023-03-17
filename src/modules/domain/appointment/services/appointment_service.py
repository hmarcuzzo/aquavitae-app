from copy import deepcopy
from typing import Optional
from uuid import UUID

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
from src.modules.domain.appointment.entities.appointment_has_appointment_goal_entity import (
    AppointmentHasAppointmentGoal,
)
from src.modules.domain.appointment.repositories.appointment_has_appointment_goal_repository import (
    AppointmentHasAppointmentGoalRepository,
)
from src.modules.domain.appointment.repositories.appointment_repository import AppointmentRepository


class AppointmentService:
    def __init__(self):
        self.appointment_repository = AppointmentRepository()
        self.appointment_has_appointment_goal_repository = AppointmentHasAppointmentGoalRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_appointment(
        self, appointment_dto: CreateAppointmentDto, db: Session
    ) -> Optional[AppointmentDto]:
        try:
            with db.begin_nested():
                goals = deepcopy(appointment_dto.goals) if appointment_dto.goals else []
                delattr(appointment_dto, "goals")

                new_appointment = await self.appointment_repository.create(appointment_dto, db)

                for goal in goals:
                    goal_dto = AppointmentHasAppointmentGoal(
                        appointment_id=new_appointment.id, appointment_goal_id=goal
                    )
                    new_appointment.appointment_has_goals += [
                        await self.appointment_has_appointment_goal_repository.create(goal_dto, db)
                    ]

            response = AppointmentDto(**new_appointment.__dict__)
            db.commit()
            return response
        except Exception as e:
            db.rollback()
            raise e

    async def get_all_appointments(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[AppointmentDto]]:
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
                "relations": ["user", "appointment_has_goals"],
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
        try:
            with db.begin_nested():
                goals = (
                    deepcopy(update_appointment_dto.goals) if update_appointment_dto.goals else []
                )
                delattr(update_appointment_dto, "goals")

                response = await self.appointment_repository.update(
                    {"where": Appointment.id == appointment_id},
                    update_appointment_dto,
                    db,
                )

                appointment_goals = await self.appointment_has_appointment_goal_repository.find(
                    {"where": AppointmentHasAppointmentGoal.appointment_id == appointment_id}, db
                )

                for appointment_goal in appointment_goals:
                    if appointment_goal.appointment_goal_id not in goals:
                        response["affected"] += (
                            await self.appointment_has_appointment_goal_repository.soft_delete(
                                str(appointment_goal.id), db
                            )
                        )["affected"]

                for goal in goals:
                    if goal not in [
                        appointment_goal.appointment_goal_id
                        for appointment_goal in appointment_goals
                    ]:
                        goal_dto = AppointmentHasAppointmentGoal(
                            appointment_id=UUID(appointment_id), appointment_goal_id=goal
                        )
                        await self.appointment_has_appointment_goal_repository.create(goal_dto, db)
                        response["affected"] += 1

            db.commit()
            return response

        except Exception as e:
            db.rollback()
            raise e

    async def delete_appointment(self, appointment_id: str, db: Session) -> Optional[UpdateResult]:
        return await self.appointment_repository.soft_delete(appointment_id, db)
