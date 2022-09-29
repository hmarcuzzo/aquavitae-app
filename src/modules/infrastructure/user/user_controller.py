from typing import List, Optional
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
from src.modules.infrastructure.database import get_db
from .dto.create_user_dto import CreateUserDto, CreateUserWithRoleDto
from .dto.update_user_dto import UpdateUserDto
from .dto.user_dto import UserDto
from .dto.user_query_dto import FindAllUserQueryDto, OrderByUserQueryDto
from .entities.user_entity import User
from .user_service import UserService
from ..auth.jwt_service import get_current_user

user_router = APIRouter(tags=["Users"], prefix="/user")

user_service = UserService()


@user_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=UserDto,
    dependencies=[Depends(Auth([UserRole.NUTRITIONIST, UserRole.ADMIN]))],
)
async def create_user(
    request: CreateUserDto, database: Session = Depends(get_db)
) -> Optional[UserDto]:
    return await user_service.create_user(request, database)


@user_router.post(
    "/with-role/create",
    status_code=HTTP_201_CREATED,
    response_model=UserDto,
    dependencies=[Depends(Auth([UserRole.ADMIN]))],
)
async def create_user_with_role(
    request: CreateUserWithRoleDto, database: Session = Depends(get_db)
) -> Optional[UserDto]:
    return await user_service.create_user_with_role(request, database)


@user_router.get(
    "/get",
    response_model=PaginationResponseDto[UserDto],
    dependencies=[Depends(Auth([UserRole.ADMIN]))],
)
async def get_all_users(
    pagination: FindManyOptions = Depends(
        GetPagination(UserDto, FindAllUserQueryDto, OrderByUserQueryDto)
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[UserDto]]:
    return await user_service.get_all_users(pagination, database)


@user_router.get(
    "/get/{id}", response_model=UserDto, dependencies=[Depends(Auth([UserRole.ADMIN]))]
)
async def get_user_by_id(id: UUID, database: Session = Depends(get_db)) -> Optional[UserDto]:
    return await user_service.find_one_user(str(id), database)


@user_router.delete("/delete", response_model=UpdateResult, dependencies=[Depends(Auth())])
async def delete_user(
    user: User = Depends(get_current_user), database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await user_service.delete_user(str(user.id), database)


@user_router.patch("/update", response_model=UpdateResult, dependencies=[Depends(Auth())])
async def update_user(
    request: UpdateUserDto,
    user: User = Depends(get_current_user),
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await user_service.update_user(str(user.id), request, database)
