from src.modules.domain.biochemical_data.repositories.biochemical_data_repository import (
    BiochemicalDataRepository,
)


class BiochemicalDataService:
    def __init__(self):
        self.biochemical_data_repository = BiochemicalDataRepository()

    # ---------------------- PUBLIC METHODS ----------------------
