from typing import List, Optional

from sqlalchemy.orm import Session

from src.core.types.exceptions_type import NotFoundException
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
        self, description: List[str], db: Session
    ) -> Optional[List[SpecificityTypeDto]]:
        specificity_types = await self.specificity_type_repository.find(
            {
                "where": [SpecificityType.description.in_(description)],
            },
            db,
        )

        if len(specificity_types) == 0:
            raise NotFoundException(msg="No Specificity Type of any kind found")

        return [SpecificityTypeDto(**st.__dict__) for st in specificity_types]

    async def create_specificity_type(
        self, specificity_type_dto: CreateSpecificityTypeDto, db: Session
    ) -> Optional[SpecificityTypeDto]:
        new_specificity_type = await self.specificity_type_repository.create(
            specificity_type_dto, db
        )

        new_specificity_type = self.specificity_type_repository.save(new_specificity_type, db)
        return SpecificityTypeDto(**new_specificity_type.__dict__)
