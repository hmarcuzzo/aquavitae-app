from typing import Optional

from sqlalchemy.orm import Session

from src.core.constants.default_values import DEFAULT_AMOUNT_GRAMS
from src.modules.domain.food.entities.food_entity import Food
from src.modules.domain.item.dto.item.create_item_dto import CreateItemDto, ListHasFoodDto
from src.modules.domain.item.dto.item.item_dto import ItemDto
from src.modules.domain.item.services.item_service import ItemService


class ItemInterface:
    def __init__(self):
        self.item_service = ItemService()

    async def create_item_from_food(self, food: Food, db: Session) -> Optional[ItemDto]:
        return await self.item_service.create_item_interface(
            CreateItemDto(
                **{
                    "description": food.description,
                    "foods": [
                        ListHasFoodDto(**{"amount_grams": DEFAULT_AMOUNT_GRAMS, "food": food.id})
                    ],
                }
            ),
            db,
        )
