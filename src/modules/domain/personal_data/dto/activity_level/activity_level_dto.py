from pydantic import conint, constr

from src.core.common.dto.base_dto import BaseDto


class ActivityLevelDto(BaseDto):
    description: constr(max_length=255)
    factor: conint()

    class Config:
        orm_mode = True
