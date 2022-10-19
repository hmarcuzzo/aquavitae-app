from src.modules.domain.meal.repositories.meals_of_plan_repository import MealsOfPlanRepository


class MealsOfPlanService:
    def __init__(self):
        self.meals_of_plan_repository = MealsOfPlanRepository()

    # ---------------------- PUBLIC METHODS ----------------------
