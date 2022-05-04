from pydantic import BaseModel, constr, EmailStr


class CreateUserDto(BaseModel):
    name: constr(min_length=2, max_length=255)
    email: EmailStr
    password: str
