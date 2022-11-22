from dataclasses import dataclass

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class Diagnosis(BaseEntity):
    main: String = Column(String(1000), nullable=False)
    secondary: String = Column(String(1000), nullable=True)
    bowel_function: String = Column(String(1000), nullable=True)
    send_by_doctor: Boolean = Column(Boolean, nullable=False, default=False)

    user_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="diagnosis")

    def __init__(
        self,
        main: String,
        send_by_doctor: Boolean,
        secondary: String = None,
        bowel_function: String = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.main = main
        self.send_by_doctor = send_by_doctor
        self.secondary = secondary
        self.bowel_function = bowel_function
