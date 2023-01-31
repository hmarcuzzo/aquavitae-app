from typing import Optional

from sqlalchemy.orm import Session

from src.modules.domain.specificity.dto.specificity_type.create_specificity_type_dto import (
    CreateSpecificityTypeDto,
)
from src.modules.domain.specificity.dto.specificity_type.specificity_type_dto import (
    SpecificityTypeDto,
)
from src.modules.domain.specificity.entities.specificity_type_entity import SpecificityType
from src.modules.domain.specificity.repositories.specificity_type_repository import (
    SpecificityTypeRepository,
)


class SpecificityTypeService:
    def __init__(self):
        self.specificity_type_repository = SpecificityTypeRepository()

    # ---------------------- PUBLIC METHODS ----------------------

    # ---------------------- INTERFACE METHODS ----------------------
    async def find_one_specificity_type_by_description(
        self, description: str, db: Session
    ) -> Optional[SpecificityTypeDto]:
        specificity_type = await self.specificity_type_repository.find_one_or_fail(
            {
                "where": SpecificityType.description == description,
            },
            db,
        )

        return SpecificityTypeDto(**specificity_type.__dict__)

    async def create_specificity_type(
        self, specificity_type_dto: CreateSpecificityTypeDto, db: Session
    ) -> Optional[SpecificityTypeDto]:
        new_specificity_type = await self.specificity_type_repository.create(
            specificity_type_dto, db
        )

        new_specificity_type = self.specificity_type_repository.save(new_specificity_type, db)
        return SpecificityTypeDto(**new_specificity_type.__dict__)
