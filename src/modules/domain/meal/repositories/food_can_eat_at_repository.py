from src.modules.domain.meal.entities.food_can_eat_at_entity import FoodCanEatAt
from src.modules.infrastructure.database.base_repository import BaseRepository


class FoodCanEatAtRepository(BaseRepository[FoodCanEatAt]):
    def __init__(self):
        super().__init__(FoodCanEatAt)
