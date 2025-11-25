"""
Interfaz del repositorio de citas
"""
from typing import Protocol, Optional, List
from datetime import date, time
from app.infrastructure.database.models.appointment import Appointment


class AppointmentRepository(Protocol):
    """Protocolo que define las operaciones del repositorio de citas"""
    
    def get_by_id(self, appointment_id: int) -> Optional[Appointment]:
        """Obtener cita por ID"""
        ...
    
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Obtener citas de un usuario"""
        ...
    
    def get_by_date(self, appointment_date: date) -> List[Appointment]:
        """Obtener citas de una fecha específica"""
        ...
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Obtener citas por estado"""
        ...
    
    def create(self, appointment: Appointment) -> Appointment:
        """Crear una nueva cita"""
        ...
    
    def update(self, appointment: Appointment) -> Appointment:
        """Actualizar una cita existente"""
        ...
    
    def delete(self, appointment_id: int) -> bool:
        """Eliminar una cita"""
        ...
    
    def check_availability(self, appointment_date: date, appointment_time: time) -> bool:
        """Verificar si un horario está disponible"""
        ...
