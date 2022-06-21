from uuid import UUID

from pydantic import BaseModel, constr, Extra, condecimal, Field


class CreateFoodDto(BaseModel):
    description: constr(max_length=255)
    proteins: condecimal(decimal_places=2)
    lipids: condecimal(decimal_places=2)
    carbohydrates: condecimal(decimal_places=2)
    energy_value: condecimal(decimal_places=2)
    potassium: condecimal(decimal_places=2)
    phosphorus: condecimal(decimal_places=2)
    sodium: condecimal(decimal_places=2)
    food_category_id: UUID = Field(alias="food_category")

    class Config:
        extra = Extra.forbid
