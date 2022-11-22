from dataclasses import dataclass

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class SpecificityType(BaseEntity):
    description: String = Column(String(1000), nullable=False)

    specificities = relationship(
        "Specificity",
        back_populates="specificity_type",
        uselist=True,
        cascade="all, delete-orphan",
    )

    def __init__(self, description: String, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = description
