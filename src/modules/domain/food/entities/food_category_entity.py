from dataclasses import dataclass

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class FoodCategory(BaseEntity):
    description: str = Column(String(255), nullable=False)
    level: int = Column(Integer, nullable=False)

    food_category_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("food_category.id"), nullable=True
    )
    food_category = relationship(
        "FoodCategory",
        primaryjoin="food_category.c.id==food_category.c.food_category_id",
        remote_side="food_category.c.id",
        backref=backref("food_categories"),
    )

    foods = relationship("Food")

    def __init__(
        self, description: str, level: int, food_category_id: UUID = None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.description = description
        self.level = level
        self.food_category_id = food_category_id
