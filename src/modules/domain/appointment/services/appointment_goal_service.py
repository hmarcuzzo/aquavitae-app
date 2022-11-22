from typing import Optional

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.appointment.dto.appointment_goal.appointment_goal_dto import (
    AppointmentGoalDto,
)
from src.modules.domain.appointment.dto.appointment_goal.create_appointment_goal_dto import (
    CreateAppointmentGoalDto,
)
from src.modules.domain.appointment.dto.appointment_goal.update_appointment_goal_dto import (
    UpdateAppointmentGoalDto,
)
from src.modules.domain.appointment.entities.appointment_goal_entity import AppointmentGoal
from src.modules.domain.appointment.repositories.appointment_goal_repository import (
    AppointmentGoalRepository,
)


class AppointmentGoalService:
    def __init__(self):
        self.appointment_goal_repository = AppointmentGoalRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_appointment_goal(
        self, appointment_goal_dto: CreateAppointmentGoalDto, db: Session
    ) -> Optional[AppointmentGoalDto]:

        new_appointment_goal = await self.appointment_goal_repository.create(
            appointment_goal_dto, db
        )

        new_appointment_goal = await self.appointment_goal_repository.save(new_appointment_goal, db)
        return AppointmentGoalDto(**new_appointment_goal.__dict__)

    async def get_all_appointment_goal(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[AppointmentGoalDto]]:
        [all_appointment_goal, total] = await self.appointment_goal_repository.find_and_count(
            pagination,
            db,
        )

        return create_pagination_response_dto(
            [
                AppointmentGoalDto(**appointment_goal.__dict__)
                for appointment_goal in all_appointment_goal
            ],
            total,
            pagination["skip"],
            pagination["take"],
        )

    async def get_appointment_goal_by_id(
        self, appointment_goal_id: str, db: Session
    ) -> Optional[AppointmentGoalDto]:
        appointment_goal = await self.appointment_goal_repository.find_one_or_fail(
            {
                "where": AppointmentGoal.id == appointment_goal_id,
            },
            db,
        )

        return AppointmentGoalDto(**appointment_goal.__dict__)

    async def update_appointment_goal(
        self,
        appointment_goal_id: str,
        update_appointment_goal_dto: UpdateAppointmentGoalDto,
        db: Session,
    ) -> Optional[UpdateResult]:
        return await self.appointment_goal_repository.update(
            {"where": AppointmentGoal.id == appointment_goal_id},
            update_appointment_goal_dto,
            db,
        )

    async def delete_appointment_goal(
        self, appointment_goal_id: str, db: Session
    ) -> Optional[UpdateResult]:
        return await self.appointment_goal_repository.soft_delete(appointment_goal_id, db)
