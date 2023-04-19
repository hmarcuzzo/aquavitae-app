from typing import List, Optional, Union
from uuid import UUID

from sqlalchemy.orm import Session

from src.core.types.update_result_type import UpdateResult
from src.modules.domain.meal.dto.item_can_eat_at.create_item_can_eat_at_dto import (
    CreateItemCanEatAtDto,
)
from src.modules.domain.meal.dto.item_can_eat_at.item_can_eat_at_dto import ItemCanEatAtDto
from src.modules.domain.meal.dto.item_can_eat_at.update_item_can_eat_at_dto import (
    UpdateItemCanEatDto,
)
from src.modules.domain.meal.entities.item_can_eat_at_entity import ItemCanEatAt
from src.modules.domain.meal.services.item_can_eat_at_service import ItemCanEatAtService


class ItemCanEatAtInterface:
    def __init__(self):
        self.item_can_eat_at_service = ItemCanEatAtService()

    async def find_one_can_eat_at(
        self, meal_type_id: UUID, item_id: UUID, db_session
    ) -> Optional[ItemCanEatAt]:
        return await self.item_can_eat_at_service.find_one_can_eat_at(
            meal_type_id, item_id, db_session
        )

    async def create_item_can_eat_at(
        self,
        item_id: UUID,
        type_of_meal_ids: List[UUID],
        db: Session,
    ) -> Optional[List[ItemCanEatAtDto]]:
        return await self.item_can_eat_at_service.create_item_can_eat_at(
            CreateItemCanEatAtDto(
                **{
                    "type_of_meal": type_of_meal_ids,
                    "item": item_id,
                }
            ),
            db,
        )

    async def update_item_can_eat_at(
        self, item_id: Union[UUID, str], types_of_meal_ids: List[UUID], db: Session
    ) -> Optional[UpdateResult]:
        return await self.item_can_eat_at_service.update_item_can_eat_at(
            UpdateItemCanEatDto(item=item_id, types_of_meal=types_of_meal_ids), db
        )
