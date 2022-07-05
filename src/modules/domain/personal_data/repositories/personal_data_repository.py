from src.modules.domain.personal_data.entities.personal_data import PersonalData
from src.modules.infrastructure.database.base_repository import BaseRepository


class PersonalDataRepository(BaseRepository[PersonalData]):
    def __init__(self):
        super().__init__(PersonalData)
