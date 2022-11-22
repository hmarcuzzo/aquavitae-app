from src.modules.domain.antecedent.entities.antecedent_entity import Antecedent
from src.modules.infrastructure.database.base_repository import BaseRepository


class AntecedentRepository(BaseRepository[Antecedent]):
    def __init__(self):
        super().__init__(Antecedent)
