from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.modules.infrastructure.database import get_db
from .user_service import UserService
from .dto.create_user_dto import CreateUserDto
from .dto.user_dto import UserDto

user_router = APIRouter(tags=['Users'], prefix='/user')

user_service = UserService()


@user_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(request: CreateUserDto, database: Session = Depends(get_db)) -> UserDto:
    return await user_service.create_user(request, database)


@user_router.get('/get')
async def get_all_users(database: Session = Depends(get_db)) -> List[UserDto]:
    return await user_service.get_all_users(database)


@user_router.get('/get/{id}')
async def get_user_by_id(id: str, database: Session = Depends(get_db)) -> UserDto:
    return await user_service.get_user_by_id(id, database)


@user_router.delete('/delete/{id}')
async def delete_user_by_id(id: str, database: Session = Depends(get_db)) -> UserDto:
    return await user_service.delete_user_by_id(id, database)
