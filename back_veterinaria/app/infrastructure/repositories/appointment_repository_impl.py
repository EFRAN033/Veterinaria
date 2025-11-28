"""
Implementación del repositorio de citas
"""
from typing import Optional, List
from datetime import date, time
from sqlalchemy.orm import Session
from app.infrastructure.database.models.appointment import Appointment


class AppointmentRepositoryImpl:
    """Implementación concreta del repositorio de citas"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, appointment_id: int) -> Optional[Appointment]:
        """Obtener cita por ID"""
        return self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
    
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Obtener citas de un usuario"""
        return self.db.query(Appointment).filter(
            Appointment.user_id == user_id
        ).offset(skip).limit(limit).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Obtener todas las citas (para veterinarios/admin)"""
        return self.db.query(Appointment).offset(skip).limit(limit).all()
    
    def get_by_date(self, appointment_date: date) -> List[Appointment]:
        """Obtener citas de una fecha específica"""
        return self.db.query(Appointment).filter(
            Appointment.appointment_date == appointment_date
        ).all()
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Obtener citas por estado"""
        return self.db.query(Appointment).filter(
            Appointment.status == status
        ).offset(skip).limit(limit).all()
    
    def create(self, appointment: Appointment) -> Appointment:
        """Crear una nueva cita"""
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment
    
    def update(self, appointment: Appointment) -> Appointment:
        """Actualizar una cita existente"""
        self.db.commit()
        self.db.refresh(appointment)
        return appointment
    
    def delete(self, appointment_id: int) -> bool:
        """Eliminar una cita"""
        appointment = self.get_by_id(appointment_id)
        if appointment:
            self.db.delete(appointment)
            self.db.commit()
            return True
        return False
    
    def check_availability(self, appointment_date: date, appointment_time: time) -> bool:
        """Verificar si un horario está disponible"""
        existing = self.db.query(Appointment).filter(
            Appointment.appointment_date == appointment_date,
            Appointment.appointment_time == appointment_time,
            Appointment.status.in_(["pending", "confirmed"])
        ).first()
        return existing is None
