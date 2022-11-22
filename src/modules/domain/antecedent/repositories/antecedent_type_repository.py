from src.modules.domain.antecedent.entities.antecedent_type_entity import AntecedentType
from src.modules.infrastructure.database.base_repository import BaseRepository


class AntecedentTypeRepository(BaseRepository[AntecedentType]):
    def __init__(self):
        super().__init__(AntecedentType)
