from src.modules.domain.diagnosis.repositories.diagnosis_repository import DiagnosisRepository


class DiagnosisService:
    def __init__(self):
        self.diagnosis_repository = DiagnosisRepository()

    # ---------------------- PUBLIC METHODS ----------------------
