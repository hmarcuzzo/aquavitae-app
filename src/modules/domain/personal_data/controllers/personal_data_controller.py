from typing import Any, List, Optional, Union
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from src.core.constants.enum.user_role import UserRole
from src.core.decorators.http_decorator import Auth
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.personal_data.dto.personal_data.create_personal_data_dto import (
    CreatePersonalDataDto,
)
from src.modules.domain.personal_data.dto.personal_data.personal_data_dto import PersonalDataDto
from src.modules.domain.personal_data.dto.personal_data.update_personal_data_dto import (
    UpdatePersonalDataDto,
)
from src.modules.domain.personal_data.services.personal_data_service import PersonalDataService
from src.modules.infrastructure.auth.auth_controller import get_current_user
from src.modules.infrastructure.database import get_db
from src.modules.infrastructure.user.entities.user_entity import User

personal_data_router = APIRouter(tags=["Personal Data"], prefix="/personal-data")

personal_data_service = PersonalDataService()


@personal_data_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=PersonalDataDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def create_personal_data(
    request: CreatePersonalDataDto, database: Session = Depends(get_db)
) -> Optional[PersonalDataDto]:
    return await personal_data_service.create_personal_data(request, database)


@personal_data_router.get(
    "/me/get",
    response_model=PersonalDataDto,
    dependencies=[Depends(Auth([UserRole.USER]))],
)
async def get_user_personal_data(
    user: User = Depends(get_current_user), database: Session = Depends(get_db)
) -> Optional[PersonalDataDto]:
    return await personal_data_service.find_one_personal_data(str(user.id), database)


@personal_data_router.get(
    "/users/get/",
    response_model=List[PersonalDataDto],
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_several_personal_data_by_user_id(
    users_id: List[UUID] = Query(default=None), database: Session = Depends(get_db)
) -> Union[list, list[PersonalDataDto]]:
    if users_id is None:
        return []

    return await personal_data_service.find_several_personal_data_by_id(
        [str(user_id) for user_id in users_id], database
    )


@personal_data_router.patch(
    "/update/{user_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def update_personal_data(
    user_id: UUID,
    request: UpdatePersonalDataDto,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await personal_data_service.update_personal_data(str(user_id), request, database)
