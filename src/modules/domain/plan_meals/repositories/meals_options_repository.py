from src.modules.domain.plan_meals.entities.meals_options_entity import MealsOptions
from src.modules.infrastructure.database.base_repository import BaseRepository


class MealsOptionsRepository(BaseRepository[MealsOptions]):
    def __init__(self):
        super().__init__(MealsOptions)
