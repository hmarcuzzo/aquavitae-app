from pydantic import BaseModel

from src.modules.infrastructure.auth.dto.token_payload_dto import TokenPayloadDto
from src.modules.infrastructure.user.dto.user_dto import UserDto


class LoginPayloadDto(BaseModel):
    user: UserDto
    token: TokenPayloadDto
