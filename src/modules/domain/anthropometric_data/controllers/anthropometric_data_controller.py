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
from src.modules.domain.anthropometric_data.dto.anthropometric_data_dto import AnthropometricDataDto
from src.modules.domain.anthropometric_data.dto.anthropometric_data_query_dto import (
    FindAllAnthropometricDataQueryDto,
    OrderByAnthropometricDataQueryDto,
)
from src.modules.domain.anthropometric_data.dto.create_anthropometric_data_dto import (
    CreateAnthropometricDataDto,
)
from src.modules.domain.anthropometric_data.dto.update_anthropometric_data_dto import (
    UpdateAnthropometricDataDto,
    UserUpdateAnthropometricDataDto,
)
from src.modules.domain.anthropometric_data.entities.anthropometric_data_entity import (
    AnthropometricData,
)
from src.modules.domain.anthropometric_data.services.anthropometric_data_service import (
    AnthropometricDataService,
)
from src.modules.infrastructure.auth.auth_controller import get_current_user
from src.modules.infrastructure.database import get_db
from src.modules.infrastructure.user.entities.user_entity import User

anthropometric_data_router = APIRouter(tags=["Anthropometric Data"], prefix="/anthropometric-data")

anthropometric_data_service = AnthropometricDataService()


@anthropometric_data_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=AnthropometricDataDto,
    dependencies=[Depends(Auth([UserRole.NUTRITIONIST]))],
)
async def create_anthropometric_data(
    request: CreateAnthropometricDataDto, database: Session = Depends(get_db)
) -> Optional[AnthropometricDataDto]:
    return await anthropometric_data_service.create_anthropometric_data(request, database)


@anthropometric_data_router.get(
    "/me/get",
    response_model=AnthropometricDataDto,
    dependencies=[Depends(Auth([UserRole.USER]))],
)
async def get_user_newest_anthropometric_data(
    user: User = Depends(get_current_user), database: Session = Depends(get_db)
) -> Optional[AnthropometricDataDto]:
    return await anthropometric_data_service.get_user_newest_anthropometric_data(
        str(user.id), database
    )


@anthropometric_data_router.get(
    "/get",
    response_model=PaginationResponseDto[AnthropometricDataDto],
    dependencies=[Depends(Auth([UserRole.NUTRITIONIST]))],
)
async def get_all_anthropometric_data_by_user_id(
    pagination: FindManyOptions = Depends(
        GetPagination(
            AnthropometricData, FindAllAnthropometricDataQueryDto, OrderByAnthropometricDataQueryDto
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[AnthropometricDataDto]]:
    return await anthropometric_data_service.get_all_user_anthropometric_data(pagination, database)


@anthropometric_data_router.get(
    "/get/{anthropometric_data_id}",
    response_model=AnthropometricDataDto,
    dependencies=[Depends(Auth([UserRole.NUTRITIONIST]))],
)
async def get_anthropometric_data_by_id(
    anthropometric_data_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[AnthropometricDataDto]]:
    return await anthropometric_data_service.get_anthropometric_data_by_id(
        str(anthropometric_data_id), database
    )


@anthropometric_data_router.patch(
    "/update/{anthropometric_data_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.NUTRITIONIST]))],
)
async def update_anthropometric_data(
    anthropometric_data_id: UUID,
    request: UpdateAnthropometricDataDto,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await anthropometric_data_service.update_anthropometric_data(
        str(anthropometric_data_id), request, database
    )


@anthropometric_data_router.patch(
    "/my-last-data/update",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.USER]))],
)
async def user_update_anthropometric_data(
    request: UserUpdateAnthropometricDataDto,
    user: User = Depends(get_current_user),
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await anthropometric_data_service.user_update_anthropometric_data(
        str(user.id), request, database
    )


@anthropometric_data_router.delete(
    "/delete/{anthropometric_data_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.NUTRITIONIST]))],
)
async def delete_anthropometric_data(
    anthropometric_data_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await anthropometric_data_service.delete_anthropometric_data(
        str(anthropometric_data_id), database
    )
