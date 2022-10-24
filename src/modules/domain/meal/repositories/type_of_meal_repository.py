from src.modules.domain.meal.entities.type_of_meal_entity import TypeOfMeal
from src.modules.infrastructure.database.base_repository import BaseRepository


class TypeOfMealRepository(BaseRepository[TypeOfMeal]):
    def __init__(self):
        super().__init__(TypeOfMeal)
