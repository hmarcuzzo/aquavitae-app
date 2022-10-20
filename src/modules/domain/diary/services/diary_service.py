from src.modules.domain.diary.repositories.diary_repository import DiaryRepository


class DiaryService:
    def __init__(self):
        self.diary_repository = DiaryRepository()

    # ---------------------- PUBLIC METHODS ----------------------
