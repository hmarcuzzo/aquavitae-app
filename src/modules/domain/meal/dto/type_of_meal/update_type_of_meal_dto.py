from typing import Optional

from pydantic import BaseModel, confloat, constr, Extra


class UpdateTypeOfMealDto(BaseModel):
    description: Optional[constr(max_length=255)]
    calories_percentage: Optional[confloat()]
    lipids_percentage: Optional[confloat()]
    proteins_percentage: Optional[confloat()]
    carbohydrates_percentage: Optional[confloat()]

    class Config:
        extra = Extra.forbid
