from src.modules.domain.antecedent.repositories.antecedent_type_repository import (
    AntecedentTypeRepository,
)


class AntecedentTypeService:
    def __init__(self):
        self.antecedent_type_repository = AntecedentTypeRepository()

    # ---------------------- PUBLIC METHODS ----------------------
