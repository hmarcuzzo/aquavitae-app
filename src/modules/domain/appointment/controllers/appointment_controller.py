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
from src.modules.domain.appointment.dto.appointment.appointment_dto import AppointmentDto
from src.modules.domain.appointment.dto.appointment.appointment_query_dto import (
    FindAllAppointmentQueryDto,
    OrderByAppointmentQueryDto,
)
from src.modules.domain.appointment.dto.appointment.create_appointment_dto import (
    CreateAppointmentDto,
)
from src.modules.domain.appointment.dto.appointment.update_appointment_dto import (
    UpdateAppointmentDto,
)
from src.modules.domain.appointment.entities.appointment_entity import Appointment
from src.modules.domain.appointment.services.appointment_service import AppointmentService
from src.modules.infrastructure.database import get_db

appointment_router = APIRouter(tags=["Appointment"], prefix="/appointment")

appointment_service = AppointmentService()


@appointment_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=AppointmentDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def create_appointment_goal(
    request: CreateAppointmentDto, database: Session = Depends(get_db)
) -> Optional[AppointmentDto]:
    return await appointment_service.create_appointment(request, database)


@appointment_router.get(
    "/get",
    response_model=PaginationResponseDto[AppointmentDto],
    response_model_exclude_unset=True,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_all_appointments(
    pagination: FindManyOptions = Depends(
        GetPagination(
            Appointment, AppointmentDto, FindAllAppointmentQueryDto, OrderByAppointmentQueryDto
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[AppointmentDto]]:
    return await appointment_service.get_all_appointments(pagination, database)


@appointment_router.get(
    "/get/{appointment_id}",
    response_model=AppointmentDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_appointment_by_id(
    appointment_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[AppointmentDto]:
    return await appointment_service.get_appointment_by_id(str(appointment_id), database)


@appointment_router.patch(
    "/update/{appointment_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def update_appointment(
    appointment_id: UUID,
    request: UpdateAppointmentDto,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await appointment_service.update_appointment(str(appointment_id), request, database)


@appointment_router.delete(
    "/delete/{appointment_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def delete_appointment(
    appointment_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await appointment_service.delete_appointment(str(appointment_id), database)
