from dataclasses import dataclass

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class Item(BaseEntity):
    description: String = Column(String(255), nullable=False)

    foods = relationship(
        "ItemHasFood", back_populates="item", uselist=True, cascade="all, delete-orphan"
    )
    meals_options = relationship(
        "MealsOptions", back_populates="item", uselist=True, cascade="all, delete-orphan"
    )

    def __init__(self, description: String(255), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = description
