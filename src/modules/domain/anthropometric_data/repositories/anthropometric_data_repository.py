from src.modules.domain.anthropometric_data.entities.anthropometric_data_entity import (
    AnthropometricData,
)
from src.modules.infrastructure.database.base_repository import BaseRepository


class AnthropometricDataRepository(BaseRepository[AnthropometricData]):
    def __init__(self):
        super().__init__(AnthropometricData)
