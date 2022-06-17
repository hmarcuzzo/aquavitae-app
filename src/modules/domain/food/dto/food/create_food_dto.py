from pydantic import BaseModel, constr, Extra, condecimal


class CreateFoodDto(BaseModel):
    description: constr(max_length=255)
    proteins: condecimal(decimal_places=2)
    lipids: condecimal(decimal_places=2)
    carbohydrates: condecimal(decimal_places=2)
    energy_value: condecimal(decimal_places=2)
    potassium: condecimal(decimal_places=2)
    phosphorus: condecimal(decimal_places=2)
    sodium: condecimal(decimal_places=2)

    class Config:
        extra = Extra.forbid
