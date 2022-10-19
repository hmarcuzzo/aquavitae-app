from src.modules.domain.forbidden_foods.entities.forbidden_foods_entity import ForbiddenFoods
from src.modules.infrastructure.database.base_repository import BaseRepository


class ForbiddenFoodsRepository(BaseRepository[ForbiddenFoods]):
    def __init__(self):
        super().__init__(ForbiddenFoods)
