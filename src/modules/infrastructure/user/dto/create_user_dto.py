from typing import Optional

from pydantic import BaseModel, constr, EmailStr, Extra, Field

from src.core.constants.enum.user_role import UserRole


class CreateUserDto(BaseModel):
    email: EmailStr
    password: constr(strip_whitespace=True)
    profile_photo: Optional[bytes]

    class Config:
        extra = Extra.forbid


class CreateUserWithRoleDto(CreateUserDto):
    role: UserRole

    class Config:
        extra = Extra.forbid
