from pydantic import constr

from src.core.common.dto.base_dto import BaseDto


class AntecedentTypeDto(BaseDto):
    description: constr(max_length=255)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
