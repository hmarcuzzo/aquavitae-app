from src.modules.domain.plan_meals.entities.meals_of_plan_entity import MealsOfPlan
from src.modules.infrastructure.database.base_repository import BaseRepository


class MealsOfPlanRepository(BaseRepository[MealsOfPlan]):
    def __init__(self):
        super().__init__(MealsOfPlan)
