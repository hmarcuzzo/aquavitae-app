from sqlalchemy import Column, Enum, String

from src.core.common.base_entity import BaseEntity
from src.core.constants.enum.user_role import UserRole
from src.core.utils.hash_utils import generate_hash, validate_hash
from src.modules.infrastructure.database import Base


class User(Base, BaseEntity):
    __tablename__ = 'user'

    name: str = Column(String(50), nullable=False)
    email: str = Column(String(120), unique=True, nullable=False)
    password: str = Column(String(120), nullable=False)
    role: UserRole = Column(Enum(UserRole), nullable=False, default=UserRole.USER)

    def __init__(self, name: str, email: str, password: str, role: UserRole = None, *args, **kwargs):
        self.name = name
        self.email = email
        self.password = generate_hash(password)
        self.role = role

    def check_password(self, password) -> bool:
        return validate_hash(self.password, password)
