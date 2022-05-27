from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.types.delete_result_type import DeleteResult
from src.modules.infrastructure.database import get_db
from .dto.update_user_dto import UpdateUserDto
from .user_service import UserService
from .dto.create_user_dto import CreateUserDto
from .dto.user_dto import UserDto

user_router = APIRouter(tags=['Users'], prefix='/user')

user_service = UserService()


@user_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(request: CreateUserDto, database: Session = Depends(get_db)) -> Optional[UserDto]:
    return await user_service.create_user(request, database)


@user_router.get('/get')
async def get_all_users(database: Session = Depends(get_db)) -> Optional[List[UserDto]]:
    return await user_service.get_all_users(database)


@user_router.get('/get/{id}')
async def get_user_by_id(id: str, database: Session = Depends(get_db)) -> Optional[UserDto]:
    return await user_service.get_user_by_id(id, database)


@user_router.delete('/delete/{id}')
async def delete_user_by_id(id: str, database: Session = Depends(get_db)) -> Optional[DeleteResult]:
    return await user_service.delete_user(id, database)


@user_router.patch('/update/{id}')
async def update_user_by_id(id: str, request: UpdateUserDto, database: Session = Depends(get_db)) -> Optional[UserDto]:
    return await user_service.update_user(id, request, database)
