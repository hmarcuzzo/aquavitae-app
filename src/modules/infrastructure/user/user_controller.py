from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.modules.infrastructure import database as db
from . import user_service
from .dto import user_dto
from .entities.user_entity import User

user_router = APIRouter(tags=['Users'], prefix='/user')

user_service = user_service.UserService()


@user_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user_registration(request: user_dto.UserDto, database: Session = Depends(db.get_db)) -> User:
    user = await user_service.verify_email_exist(request.email, database)

    if user:
        raise HTTPException(
            status_code=400,
            detail='The user with this email already exists in the system.'
        )

    new_user = await user_service.new_user_register(request, database)
    return new_user
