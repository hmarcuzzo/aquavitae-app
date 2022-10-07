from src.modules.domain.appointment.entities.appointment_entity import Appointment
from src.modules.infrastructure.database.base_repository import BaseRepository


class AppointmentRepository(BaseRepository[Appointment]):
    def __init__(self):
        super().__init__(Appointment)
