from src.modules.domain.nutritional_plan.repositories.nutritional_plan_repository import (
    NutritionalPlanRepository,
)


class NutritionalPlanService:
    def __init__(self):
        self.nutritional_plan_repository = NutritionalPlanRepository()

    # ---------------------- PUBLIC METHODS ----------------------
