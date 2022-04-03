from typing import Optional

from sqlalchemy.orm import Session

from .dto.user_dto import UserDto
from .entities.user_entity import User
from .user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    async def verify_email_exist(self, email: str, db_session: Session) -> Optional[User]:
        return self.user_repository.find_user_by_email(email, db_session)

    async def new_user_register(self, user_dto: UserDto, db_session: Session) -> User:
        new_user = User(name=user_dto.name, email=user_dto.email, password=user_dto.password)
        return self.user_repository.create_user(new_user, db_session)
