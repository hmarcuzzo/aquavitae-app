from dataclasses import dataclass

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class Antecedent(BaseEntity):
    description: String = Column(String(1000), nullable=False)

    antecedent_type_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("antecedent_type.id", ondelete="CASCADE"), nullable=False
    )
    antecedent_type = relationship("AntecedentType", back_populates="antecedents")

    user_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="antecedents")

    def __init__(
        self, description: String(255), antecedent_type_id: UUID, user_id: UUID, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.description = description
        self.antecedent_type_id = antecedent_type_id
        self.user_id = user_id
