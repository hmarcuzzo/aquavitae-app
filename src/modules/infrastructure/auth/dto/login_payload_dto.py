from datetime import datetime

from pydantic import BaseModel

from src.modules.infrastructure.user.dto.user_dto import UserDto


class LoginPayloadDto(BaseModel):
    user: UserDto
    expires_in: datetime
    access_token: str
    token_type: str = "Bearer"
