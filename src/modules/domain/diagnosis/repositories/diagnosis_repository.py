from src.modules.domain.diagnosis.entities.diagnosis_entity import Diagnosis
from src.modules.infrastructure.database.base_repository import BaseRepository


class DiagnosisRepository(BaseRepository[Diagnosis]):
    def __init__(self):
        super().__init__(Diagnosis)
