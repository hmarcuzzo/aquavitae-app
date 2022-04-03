from sqlalchemy import Column, Integer, String

from src.core.utils.hash_utils import generate_hash, validate_hash
from src.modules.infrastructure.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

    def __init__(self, name, email, password, *args, **kwargs):
        self.name = name
        self.email = email
        self.password = generate_hash(password)

    def check_password(self, password):
        return validate_hash(self.password, password)
