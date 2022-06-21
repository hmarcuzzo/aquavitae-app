from pydantic import BaseModel, constr, EmailStr, Extra


class CreateUserDto(BaseModel):
    name: constr(min_length=2, max_length=255, strip_whitespace=True)
    email: EmailStr
    password: constr(strip_whitespace=True)

    class Config:
        extra = Extra.forbid
