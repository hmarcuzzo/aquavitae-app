from typing import Optional

from sqlalchemy.orm import Session

from src.modules.domain.specificity.dto.specificity_type.create_specificity_type_dto import (
    CreateSpecificityTypeDto,
)
from src.modules.domain.specificity.dto.specificity_type.specificity_type_dto import (
    SpecificityTypeDto,
)
from src.modules.domain.specificity.services.specificity_type_service import SpecificityTypeService


class SpecificityTypeInterface:
    def __init__(self):
        self.specificity_type_service = SpecificityTypeService()

    async def find_one_specificity_type_by_description(
        self, description: str, db: Session
    ) -> Optional[SpecificityTypeDto]:
        return await self.specificity_type_service.find_one_specificity_type_by_description(
            description, db
        )

    async def create_specificity_type(
        self, description: str, db: Session
    ) -> Optional[SpecificityTypeDto]:
        return await self.specificity_type_service.create_specificity_type(
            CreateSpecificityTypeDto(**{"description": description}), db
        )
