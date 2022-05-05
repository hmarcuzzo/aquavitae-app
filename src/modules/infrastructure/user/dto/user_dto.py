from src.core.common.dto.base_dto import BaseDto
from src.core.constants.enum.user_role import UserRole
from src.modules.infrastructure.user.entities.user_entity import User


class UserDto(BaseDto):
    def __init__(self, user_entity: User):
        super().__init__(user_entity)

        self.name: str = user_entity.name
        self.email: str = user_entity.email
        self.role: UserRole = user_entity.role

    class Config:
        orm_mode = True
