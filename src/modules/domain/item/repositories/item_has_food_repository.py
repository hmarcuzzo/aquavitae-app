from src.modules.domain.item.entities.item_has_food import ItemHasFood
from src.modules.infrastructure.database.base_repository import BaseRepository


class ItemHasFoodRepository(BaseRepository[ItemHasFood]):
    def __init__(self):
        super().__init__(ItemHasFood)
