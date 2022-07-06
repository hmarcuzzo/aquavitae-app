from dataclasses import dataclass

from sqlalchemy import Column, DateTime, Enum, event, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils import has_changes

from src.core.constants.enum.user_role import UserRole
from src.core.utils.hash_utils import generate_hash, validate_hash
from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class User(BaseEntity):
    name: str = Column(String(255), nullable=False)
    email: str = Column(String(120), nullable=False)
    password: str = Column(String(120), nullable=False)
    role: UserRole = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    last_access: DateTime = Column(DateTime(timezone=True), nullable=True)

    personal_data = relationship(
        "PersonalData", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    __table_args__ = (UniqueConstraint("email", "deleted_at", name="unique_user_email_active"),)

    def __init__(
        self, name: str, email: str, password: str, role: UserRole = UserRole.USER, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def check_password(self, password: str) -> bool:
        return validate_hash(password, self.password)


@event.listens_for(User, "before_insert")
@event.listens_for(User, "before_update")
def before_insert(mapper, connection, target: User) -> None:
    if has_changes(target, "password"):
        target.password = generate_hash(target.password)

    if has_changes(target, "last_access"):
        target.updated_at = target.last_access
