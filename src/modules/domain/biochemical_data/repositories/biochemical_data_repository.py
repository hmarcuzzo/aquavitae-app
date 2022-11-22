from src.modules.domain.biochemical_data.entities.biochemical_data_entity import BiochemicalData
from src.modules.infrastructure.database.base_repository import BaseRepository


class BiochemicalDataRepository(BaseRepository[BiochemicalData]):
    def __init__(self):
        super().__init__(BiochemicalData)
