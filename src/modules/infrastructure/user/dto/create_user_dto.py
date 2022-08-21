from pydantic import BaseModel, constr, EmailStr, Extra


class CreateUserDto(BaseModel):
    email: EmailStr
    password: constr(strip_whitespace=True)

    class Config:
        extra = Extra.forbid
