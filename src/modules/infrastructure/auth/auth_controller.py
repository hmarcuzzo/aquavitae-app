from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.modules.infrastructure.database import get_db
from .auth_service import AuthService
from .dto.login_payload_dto import LoginPayloadDto

auth_router = APIRouter(tags=['Auth'])

auth_service = AuthService()


@auth_router.post('/login', response_model=LoginPayloadDto)
async def login(
        request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Optional[LoginPayloadDto]:
    return await auth_service.login_user(request, db)


# @auth_router.get(
#     '/me',
#     response_model=UserDto,
#     dependencies=[Depends(Auth())]
# )
# async def get_current_user(
#         user: User = Depends(get_current_user)
# ) -> Optional[User]:
#     return user
