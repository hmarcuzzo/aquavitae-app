from .entities.user_entity import User
from ..database.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
