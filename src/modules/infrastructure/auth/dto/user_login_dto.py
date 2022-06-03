from pydantic import BaseModel, EmailStr, Extra


class UserLoginDto(BaseModel):
    email: EmailStr
    password: str

    class Config:
        extra = Extra.forbid
