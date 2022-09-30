from dataclasses import dataclass

from sqlalchemy import Column, Date, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.constants.enum.appointment_status import AppointmentStatus
from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class Appointment(BaseEntity):
    date: Date = Column(Date, nullable=False)
    status: AppointmentStatus = Column(
        Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.SCHEDULED
    )

    user_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="appointments")

    def __init__(
        self,
        date: Date,
        user_id: UUID,
        status: AppointmentStatus = AppointmentStatus.SCHEDULED,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.date = date
        self.user_id = user_id
        self.status = status