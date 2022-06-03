from typing import List

from fastapi import Depends

from src.core.constants.enum.user_role import UserRole
from src.core.types.exceptions_type import ForbiddenException
from src.modules.infrastructure.auth.jwt_service import get_current_user
from src.modules.infrastructure.user.entities.user_entity import User


class Auth:
    def __init__(self, roles: List[UserRole] = None, public: bool = False):
        self.roles = roles
        self.public = public

    def __call__(self, user: User = Depends(get_current_user)):
        if not self.public and self.roles and user.role not in self.roles:
            raise ForbiddenException('You do not have permission to access this resource', ['User', 'role'])
