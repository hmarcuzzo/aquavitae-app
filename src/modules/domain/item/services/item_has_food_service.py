from src.modules.domain.item.repositories.item_has_food_repository import ItemHasFoodRepository


class ItemHasFoodService:
    def __init__(self):
        self.item_has_food_repository = ItemHasFoodRepository()

    # ---------------------- PUBLIC METHODS ----------------------
