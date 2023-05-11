from dataclasses import dataclass

from sqlalchemy import Column, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.constants.enum.appointment_status import AppointmentStatus
from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class Appointment(BaseEntity):
    date: DateTime = Column(DateTime(timezone=True), nullable=False)
    status: AppointmentStatus = Column(
        Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.SCHEDULED
    )

    user_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship(
        "User",
        back_populates="user_appointments",
        primaryjoin="Appointment.user_id == User.id",
        foreign_keys=[user_id],
    )

    nutritionist_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    nutritionist = relationship(
        "User",
        back_populates="nutritionist_appointments",
        primaryjoin="Appointment.nutritionist_id == User.id",
        foreign_keys=[nutritionist_id],
    )

    appointment_has_goals = relationship(
        "AppointmentHasAppointmentGoal",
        back_populates="appointment",
        uselist=True,
        cascade="all, delete-orphan",
    )

    biochemical_data = relationship(
        "BiochemicalData",
        back_populates="appointment",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __init__(
        self,
        date: DateTime,
        user_id: UUID,
        status: AppointmentStatus = AppointmentStatus.SCHEDULED,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.date = date
        self.user_id = user_id
        self.status = status
