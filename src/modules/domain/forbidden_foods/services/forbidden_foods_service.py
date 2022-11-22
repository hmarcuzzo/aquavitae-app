from src.modules.domain.forbidden_foods.repositories.forbidden_foods_repository import (
    ForbiddenFoodsRepository,
)


class ForbiddenFoodsService:
    def __init__(self):
        self.forbidden_foods_repository = ForbiddenFoodsRepository()

    # ---------------------- PUBLIC METHODS ----------------------
