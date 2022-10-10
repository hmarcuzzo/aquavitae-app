from src.modules.domain.antecedent.repositories.antecedent_repository import AntecedentRepository


class AntecedentService:
    def __init__(self):
        self.antecedent_repository = AntecedentRepository()

    # ---------------------- PUBLIC METHODS ----------------------
