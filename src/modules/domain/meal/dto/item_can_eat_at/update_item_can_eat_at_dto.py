from typing import Optional
from uuid import UUID

from pydantic import BaseModel, conlist, Extra, Field


class UpdateItemCanEatDto(BaseModel):
    types_of_meal_id: conlist(UUID, min_items=1) = Field(alias="types_of_meal")
    item_id: UUID = Field(alias="item")

    class Config:
        extra = Extra.forbid
