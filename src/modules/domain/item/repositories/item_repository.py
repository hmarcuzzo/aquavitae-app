from src.modules.domain.item.entities.item_entity import Item
from src.modules.infrastructure.database.base_repository import BaseRepository


class ItemRepository(BaseRepository[Item]):
    def __init__(self):
        super().__init__(Item)
