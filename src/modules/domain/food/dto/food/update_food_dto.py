from typing import Optional

from pydantic import BaseModel, condecimal, constr, Extra


class UpdateFoodDto(BaseModel):
    description: Optional[constr(max_length=255)]
    proteins: Optional[condecimal(decimal_places=2)]
    lipids: Optional[condecimal(decimal_places=2)]
    carbohydrates: Optional[condecimal(decimal_places=2)]
    energy_value: Optional[condecimal(decimal_places=2)]
    potassium: Optional[condecimal(decimal_places=2)]
    phosphorus: Optional[condecimal(decimal_places=2)]
    sodium: Optional[condecimal(decimal_places=2)]

    class Config:
        extra = Extra.forbid
