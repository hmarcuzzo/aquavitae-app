from typing import List

from fastapi import Depends

from src.core.constants.enum.user_role import UserRole
from src.core.types.exceptions_type import ForbiddenException
from src.modules.infrastructure.auth.jwt_service import get_current_user
from src.modules.infrastructure.user import User


class Auth:
    def __init__(self, roles: List[UserRole] = None):
        self.roles = roles

    def __call__(self, user: User = Depends(get_current_user)):
        if self.roles and user.role not in self.roles:
            raise ForbiddenException('You do not have permission to access this resource')
