from src.modules.domain.nutritional_plan.entities.nutritional_plan_entity import NutritionalPlan
from src.modules.infrastructure.database.base_repository import BaseRepository


class NutritionalPlanRepository(BaseRepository[NutritionalPlan]):
    def __init__(self):
        super().__init__(NutritionalPlan)
