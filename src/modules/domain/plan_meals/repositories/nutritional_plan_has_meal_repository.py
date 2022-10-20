from src.modules.domain.plan_meals.entities.nutritional_plan_has_meal_entity import (
    NutritionalPlanHasMeal,
)
from src.modules.infrastructure.database.base_repository import BaseRepository


class NutritionalPlanHasMealRepository(BaseRepository[NutritionalPlanHasMeal]):
    def __init__(self):
        super().__init__(NutritionalPlanHasMeal)
