from src.modules.domain.item.repositories.item_repository import ItemRepository


class ItemService:
    def __init__(self):
        self.item_repository = ItemRepository()

    # ---------------------- PUBLIC METHODS ----------------------
