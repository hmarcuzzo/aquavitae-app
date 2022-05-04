from enum import Enum

from src.core.common.dto.base_dto import BaseDto
from src.core.constants.enum.user_role import UserRole
from src.modules.infrastructure.user.entities.user_entity import User


class UserDto(BaseDto):
    name: str
    email: str
    role: UserRole

    def __init__(self, user_entity: User):
        super().__init__(user_entity)

        self.name = user_entity.name
        self.email = user_entity.email
        self.role = user_entity.role

    class Config:
        orm_mode = True
