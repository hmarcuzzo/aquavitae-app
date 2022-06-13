from dataclasses import dataclass

from sqlalchemy import Column, String, Float

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class Food(BaseEntity):
    description: str = Column(String(255), nullable=False)
    proteins: float = Column(Float(2), nullable=False)
    lipids: float = Column(Float(2), nullable=False)
    carbohydrates: float = Column(Float(2), nullable=False)
    energy_value: float = Column(Float(2), nullable=False)
    potassium: float = Column(Float(2), nullable=False)
    phosphorus: float = Column(Float(2), nullable=False)
    sodium: float = Column(Float(2), nullable=False)

    def __init__(
        self,
        description: str,
        proteins: int,
        lipids: int,
        carbohydrates: int,
        energy_value: int,
        potassium: int,
        phosphorus: int,
        sodium: int,
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
