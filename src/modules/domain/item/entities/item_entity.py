from dataclasses import dataclass

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class Item(BaseEntity):
    description: str = Column(String(255), nullable=False)

    foods = relationship(
        "ItemHasFood", back_populates="item", uselist=True, cascade="all, delete-orphan"
    )
    meals_options = relationship(
        "MealsOptions", back_populates="item", uselist=True, cascade="all, delete-orphan"
    )
    diary_meals = relationship(
        "Diary", back_populates="item", uselist=True, cascade="all, delete-orphan"
    )
    can_eat_at = relationship(
        "ItemCanEatAt", back_populates="item", uselist=True, cascade="all, delete-orphan"
    )

    def __init__(self, description: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = description
