from pydantic import BaseModel, constr, EmailStr


class UserDto(BaseModel):
    name: constr(min_length=2, max_length=50)
    email: EmailStr
    password: str
