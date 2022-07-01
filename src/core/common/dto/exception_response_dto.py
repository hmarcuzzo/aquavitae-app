from datetime import datetime
from typing import List

from pydantic import BaseModel, Extra, Field


class DetailResponseDto(BaseModel):
    loc: List[str] = Field(title="Location")
    msg: str = Field(title="Message")
    type: str = Field(title="Error Type")

    class Config:
        extra = Extra.forbid


class ExceptionResponseDto(BaseModel):
    detail: List[DetailResponseDto]
    status_code: int = 422
    timestamp: datetime = Field(title="Timestamp of the Request")
    path: str = Field(title="Request Path")
    method: str = Field(title="Request Method")

    class Config:
        extra = Extra.forbid
