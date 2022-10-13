from src.modules.domain.specificity.repositories.specificity_repository import SpecificityRepository


class SpecificityService:
    def __init__(self):
        self.specificity_repository = SpecificityRepository()

    # ---------------------- PUBLIC METHODS ----------------------
