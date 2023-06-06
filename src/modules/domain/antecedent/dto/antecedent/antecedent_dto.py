from typing import Optional, Union
from uuid import UUID

from pydantic import constr

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.antecedent.dto.antecedent_type.antecedent_type_dto import AntecedentTypeDto
from src.modules.infrastructure.user.dto.user_dto import UserDto


class AntecedentDto(BaseDto):
    description: constr(max_length=255)
    antecedent_type: Optional[Union[AntecedentTypeDto, UUID]]
    user: Optional[Union[UserDto, UUID]]

    def __init__(self, **kwargs):
        if "antecedent_type" not in kwargs and "antecedent_type_id" in kwargs:
            kwargs["antecedent_type"] = kwargs["antecedent_type_id"]
        if "user" not in kwargs and "user_id" in kwargs:
            kwargs["user"] = kwargs["user_id"]
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
