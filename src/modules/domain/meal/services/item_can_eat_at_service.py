from typing import List, Optional
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
from src.modules.domain.meal.repositories.item_can_eat_at_repository import ItemCanEatAtRepository
from src.modules.infrastructure.database.control_transaction import keep_nested_transaction


class ItemCanEatAtService:
    def __init__(self):
        self.item_can_eat_at_repository = ItemCanEatAtRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_item_can_eat_at(
        self, item_can_eat_at_dto: CreateItemCanEatAtDto, db: Session
    ) -> Optional[List[ItemCanEatAtDto]]:
        try:
            all_item_can_eat_at = []
            with keep_nested_transaction(db):
                for meal_type_id in item_can_eat_at_dto.type_of_meal_id:
                    new_item_can_eat_at = await self.item_can_eat_at_repository.create(
                        ItemCanEatAt(
                            type_of_meal_id=meal_type_id, item_id=item_can_eat_at_dto.item_id
                        ),
                        db,
                    )
                    new_item_can_eat_at = self.item_can_eat_at_repository.save(
                        new_item_can_eat_at, db
                    )
                    all_item_can_eat_at.append(ItemCanEatAtDto(**new_item_can_eat_at.__dict__))

            db.commit()
            return all_item_can_eat_at
        except Exception as e:
            db.rollback()
            raise e

    async def find_one_can_eat_at(
        self, meal_type_id: UUID, item_id: UUID, db_session
    ) -> Optional[ItemCanEatAt]:
        return await self.item_can_eat_at_repository.find_one_or_fail(
            {
                "where": [
                    ItemCanEatAt.type_of_meal_id == meal_type_id,
                    ItemCanEatAt.item_id == item_id,
                ]
            },
            db_session,
        )

    async def update_item_can_eat_at(
        self, update_item_can_eat_dto: UpdateItemCanEatDto, db
    ) -> Optional[UpdateResult]:
        item_can_eat_at = await self.item_can_eat_at_repository.find(
            {"where": ItemCanEatAt.item_id == update_item_can_eat_dto.item_id}, db
        )
        can_eat_at_meals_id = [can_eat_at.type_of_meal_id for can_eat_at in item_can_eat_at]

        response = UpdateResult(raw=[], affected=0, generatedMaps=[])

        with keep_nested_transaction(db):
            for meal_id in update_item_can_eat_dto.types_of_meal_id:
                if meal_id in can_eat_at_meals_id:
                    # Ignore types of meal already in the database
                    index = can_eat_at_meals_id.index(meal_id)
                    del can_eat_at_meals_id[index]

                else:
                    # Create new types of meal
                    response["affected"] += len(
                        await self.create_item_can_eat_at(
                            CreateItemCanEatAtDto(
                                item=update_item_can_eat_dto.item_id, type_of_meal=[meal_id]
                            ),
                            db,
                        )
                    )

            # Delete types of meal that are not in the update list
            if len(can_eat_at_meals_id) > 0:
                for meal_id in can_eat_at_meals_id:
                    response["affected"] += (
                        await self.item_can_eat_at_repository.soft_delete(
                            {
                                "where": [
                                    ItemCanEatAt.item_id == update_item_can_eat_dto.item_id,
                                    ItemCanEatAt.type_of_meal_id == meal_id,
                                ]
                            },
                            db,
                        )
                    )["affected"]

        db.commit()
        return response
