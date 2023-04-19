from src.modules.domain.item.services.item_service import ItemService


class ItemInterface:
    def __init__(self):
        self.item_service = ItemService()
