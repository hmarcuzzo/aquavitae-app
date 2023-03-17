from pydantic import BaseModel, confloat, constr, Extra


class CreateTypeOfMealDto(BaseModel):
    description: constr(max_length=255)
    calories_percentage: confloat()
    lipids_percentage: confloat()
    proteins_percentage: confloat()
    carbohydrates_percentage: confloat()

    class Config:
        extra = Extra.forbid
