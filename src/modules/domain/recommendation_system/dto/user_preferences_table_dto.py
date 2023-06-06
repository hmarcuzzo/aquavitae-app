from uuid import UUID

from pydantic import BaseModel, conint, constr

from src.modules.domain.food.dto.food.food_dto import FoodDto


class DetailedUserPreferencesTable(FoodDto):
    score: conint()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Config:
        orm_mode = True


class SimplifiedUserPreferencesTable(BaseModel):
    id: UUID
    description: constr(max_length=255)
    score: conint()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
