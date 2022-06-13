from datetime import datetime

from pydantic import BaseModel


class TokenPayloadDto(BaseModel):
    expires_in: datetime
    access_token: str
    token_type: str = "bearer"
