from datetime import date
from uuid import UUID

from pydantic import BaseModel, Extra, Field


class CreateNutritionalPlanHasMealDto(BaseModel):
    meal_date: date
    nutritional_plan_id: UUID = Field(alias="nutritional_plan")
    meals_of_plan_id: UUID = Field(alias="meals_of_plan")

    class Config:
        extra = Extra.forbid
