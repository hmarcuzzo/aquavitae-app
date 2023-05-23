from src.modules.domain.meal.entities.item_can_eat_at_entity import ItemCanEatAt
from src.modules.infrastructure.database.base_repository import BaseRepository


class ItemCanEatAtRepository(BaseRepository[ItemCanEatAt]):
    def __init__(self):
        super().__init__(ItemCanEatAt)
