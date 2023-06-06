from typing import Optional

from pydantic import confloat, constr

from src.core.common.dto.base_dto import BaseDto


class TypeOfMealDto(BaseDto):
    description: constr(max_length=255)
    calories_percentage: Optional[confloat()]
    lipids_percentage: Optional[confloat()]
    proteins_percentage: Optional[confloat()]
    carbohydrates_percentage: Optional[confloat()]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
