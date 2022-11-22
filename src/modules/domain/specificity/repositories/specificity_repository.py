from src.modules.domain.specificity.entities.specificity_entity import Specificity
from src.modules.infrastructure.database.base_repository import BaseRepository


class SpecificityRepository(BaseRepository[Specificity]):
    def __init__(self):
        super().__init__(Specificity)
