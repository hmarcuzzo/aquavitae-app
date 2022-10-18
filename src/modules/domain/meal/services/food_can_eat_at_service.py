from src.modules.domain.meal.repositories.food_can_eat_at_repository import FoodCanEatAtRepository


class FoodCanEatAtService:
    def __init__(self):
        self.food_can_eat_at_repository = FoodCanEatAtRepository()

    # ---------------------- PUBLIC METHODS ----------------------
