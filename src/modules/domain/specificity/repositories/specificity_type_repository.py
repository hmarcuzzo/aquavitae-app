from src.modules.domain.specificity.entities.specificity_type_entity import SpecificityType
from src.modules.infrastructure.database.base_repository import BaseRepository


class SpecificityTypeRepository(BaseRepository[SpecificityType]):
    def __init__(self):
        super().__init__(SpecificityType)
