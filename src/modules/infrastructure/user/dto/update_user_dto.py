from typing import Optional

from pydantic import BaseModel, constr, EmailStr, Extra


class UpdateUserDto(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]

    class Config:
        extra = Extra.forbid
