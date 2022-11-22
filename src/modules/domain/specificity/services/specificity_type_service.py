from src.modules.domain.specificity.repositories.specificity_type_repository import (
    SpecificityTypeRepository,
)


class SpecificityTypeService:
    def __init__(self):
        self.specificity_type_repository = SpecificityTypeRepository()

    # ---------------------- PUBLIC METHODS ----------------------
