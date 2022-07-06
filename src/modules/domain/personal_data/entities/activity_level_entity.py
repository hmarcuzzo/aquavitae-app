from dataclasses import dataclass

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class ActivityLevel(BaseEntity):
    description: str = Column(String(255), nullable=False)
    factor: int = Column(Integer, nullable=False)

    personal_data = relationship(
        "PersonalData",
        back_populates="activity_level",
    )

    def __init__(self, description: str, factor: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = description
        self.factor = factor
