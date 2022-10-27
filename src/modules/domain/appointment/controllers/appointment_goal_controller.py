from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from src.core.common.dto.pagination_response_dto import PaginationResponseDto
from src.core.constants.enum.user_role import UserRole
from src.core.decorators.http_decorator import Auth
from src.core.decorators.pagination_decorator import GetPagination
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.appointment.dto.appointment_goal.appointment_goal_dto import (
    AppointmentGoalDto,
)
from src.modules.domain.appointment.dto.appointment_goal.appointment_goal_query_dto import (
    FindAllAppointmentGoalQueryDto,
    OrderByAppointmentGoalQueryDto,
)
from src.modules.domain.appointment.dto.appointment_goal.create_appointment_goal_dto import (
    CreateAppointmentGoalDto,
)
from src.modules.domain.appointment.dto.appointment_goal.update_appointment_goal_dto import (
    UpdateAppointmentGoalDto,
)
from src.modules.domain.appointment.entities.appointment_goal_entity import AppointmentGoal
from src.modules.domain.appointment.services.appointment_goal_service import AppointmentGoalService
from src.modules.infrastructure.database import get_db

appointment_goal_router = APIRouter(tags=["Appointment Goal"], prefix="/appointment-goal")

appointment_goal_service = AppointmentGoalService()


@appointment_goal_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=AppointmentGoalDto,
    dependencies=[Depends(Auth([UserRole.ADMIN]))],
)
async def create_appointment_goal(
    request: CreateAppointmentGoalDto, database: Session = Depends(get_db)
) -> Optional[AppointmentGoalDto]:
    return await appointment_goal_service.create_appointment_goal(request, database)


@appointment_goal_router.get(
    "/get",
    response_model=PaginationResponseDto[AppointmentGoalDto],
    dependencies=[Depends(Auth([UserRole.NUTRITIONIST, UserRole.ADMIN]))],
)
async def get_all_appointment_goal(
    pagination: FindManyOptions = Depends(
        GetPagination(
            AppointmentGoal, FindAllAppointmentGoalQueryDto, OrderByAppointmentGoalQueryDto
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[AppointmentGoalDto]]:
    return await appointment_goal_service.get_all_appointment_goal(pagination, database)


@appointment_goal_router.get(
    "/get/{appointment_goal_id}",
    response_model=AppointmentGoalDto,
    dependencies=[Depends(Auth([UserRole.NUTRITIONIST, UserRole.ADMIN]))],
)
async def get_appointment_goal_by_id(
    appointment_goal_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[AppointmentGoalDto]:
    return await appointment_goal_service.get_appointment_goal_by_id(
        str(appointment_goal_id), database
    )


@appointment_goal_router.patch(
    "/update/{appointment_goal_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN]))],
)
async def update_appointment_goal(
    appointment_goal_id: UUID,
    request: UpdateAppointmentGoalDto,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await appointment_goal_service.update_appointment_goal(
        str(appointment_goal_id), request, database
    )


@appointment_goal_router.delete(
    "/delete/{appointment_goal_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN]))],
)
async def delete_appointment_goal(
    appointment_goal_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await appointment_goal_service.delete_appointment_goal(
        str(appointment_goal_id), database
    )
