from typing import List

from fastapi import Depends

from src.core.constants.enum.user_role import UserRole
from src.core.types.exceptions_type import ForbiddenException
from src.modules.infrastructure.auth.jwt_service import get_current_user_role


class Auth:
    def __init__(self, roles: List[UserRole] = None):
        self.roles = roles

    def __call__(self, user_role: UserRole = Depends(get_current_user_role)):
        if self.roles and user_role not in self.roles:
            raise ForbiddenException('You do not have permission to access this resource')
