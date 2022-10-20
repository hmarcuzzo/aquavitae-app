from src.modules.domain.diary.entities.diary_entity import Diary
from src.modules.infrastructure.database.base_repository import BaseRepository


class DiaryRepository(BaseRepository[Diary]):
    def __init__(self):
        super().__init__(Diary)
