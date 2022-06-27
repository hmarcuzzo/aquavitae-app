from dataclasses import dataclass

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class Food(BaseEntity):
    description: String = Column(String(255), nullable=False)
    proteins: Float(2) = Column(Float(2), nullable=False)
    lipids: Float(2) = Column(Float(2), nullable=False)
    carbohydrates: Float(2) = Column(Float(2), nullable=False)
    energy_value: Float(2) = Column(Float(2), nullable=False)
    potassium: Float(2) = Column(Float(2), nullable=False)
    phosphorus: Float(2) = Column(Float(2), nullable=False)
    sodium: Float(2) = Column(Float(2), nullable=False)

    food_category_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("food_category.id", ondelete="CASCADE"), nullable=False
    )
    food_category = relationship("FoodCategory", back_populates="foods")

    def __init__(
        self,
        description: String(255),
        proteins: Float(2),
        lipids: Float(2),
        carbohydrates: Float(2),
        energy_value: Float(2),
        potassium: Float(2),
        phosphorus: Float(2),
        sodium: Float(2),
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.description = description
        self.proteins = proteins
        self.lipids = lipids
        self.carbohydrates = carbohydrates
        self.energy_value = energy_value
        self.potassium = potassium
        self.phosphorus = phosphorus
        self.sodium = sodium
