from src.modules.domain.plan_meals.repositories.nutritional_plan_has_meal_repository import (
    NutritionalPlanHasMealRepository,
)


class NutritionalPlanHasMealService:
    def __init__(self):
        self.nutritional_plan_has_meal_repository = NutritionalPlanHasMealRepository()

    # ---------------------- PUBLIC METHODS ----------------------
