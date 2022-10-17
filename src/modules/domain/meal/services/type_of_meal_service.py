from src.modules.domain.meal.repositories.type_of_meal_repository import TypeOfMealRepository


class TypeOfMealService:
    def __init__(self):
        self.type_of_meal_repository = TypeOfMealRepository()

    # ---------------------- PUBLIC METHODS ----------------------
