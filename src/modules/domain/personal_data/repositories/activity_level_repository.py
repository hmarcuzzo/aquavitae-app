from src.modules.domain.personal_data.entities.activity_level import ActivityLevel
from src.modules.infrastructure.database.base_repository import BaseRepository


class ActivityLevelRepository(BaseRepository[ActivityLevel]):
    def __init__(self):
        super().__init__(ActivityLevel)
