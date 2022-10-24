from src.modules.domain.plan_meals.repositories.meals_options_repository import (
    MealsOptionsRepository,
)


class MealsOptionsService:
    def __init__(self):
        self.meals_options_repository = MealsOptionsRepository()

    # ---------------------- PUBLIC METHODS ----------------------
