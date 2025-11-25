"""
Servicio de gestión de citas
Contiene la lógica de negocio para CRUD de citas con validaciones
"""
from typing import List
from sqlalchemy.orm import Session
from datetime import date, time
from app.application.dtos.appointment_dto import AppointmentCreateDTO, AppointmentUpdateDTO, AppointmentDTO
from app.infrastructure.repositories.appointment_repository_impl import AppointmentRepositoryImpl
from app.infrastructure.repositories.service_repository_impl import ServiceRepositoryImpl
from app.infrastructure.database.models.appointment import Appointment
from app.core.exceptions import NotFoundException, ValidationException, BusinessRuleException


class AppointmentService:
    """Servicio de gestión de citas"""
    
    def __init__(self, db: Session):
        self.db = db
        self.appointment_repo = AppointmentRepositoryImpl(db)
        self.service_repo = ServiceRepositoryImpl(db)
    
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[AppointmentDTO]:
        """Obtener citas de un usuario"""
        appointments = self.appointment_repo.get_by_user(user_id, skip=skip, limit=limit)
        return [AppointmentDTO.model_validate(appointment) for appointment in appointments]
    
    def get_history_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[AppointmentDTO]:
        """Obtener historial de citas (completadas, canceladas o pasadas)"""
        appointments = self.appointment_repo.get_by_user(user_id, skip=0, limit=1000)
        
        history = [
            app for app in appointments 
            if app.status in ["completed", "cancelled"] or 
            (app.appointment_date < date.today() and app.status != "cancelled")
        ]
        
        return [AppointmentDTO.model_validate(app) for app in history[skip:skip+limit]]

    def get_pending_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[AppointmentDTO]:
        """Obtener citas pendientes (futuras y no canceladas)"""
        appointments = self.appointment_repo.get_by_user(user_id, skip=0, limit=1000)
        
        pending = [
            app for app in appointments 
            if app.status in ["pending", "confirmed"] and app.appointment_date >= date.today()
        ]
        
        return [AppointmentDTO.model_validate(app) for app in pending[skip:skip+limit]]
    
    def get_by_id(self, appointment_id: int, user_id: int) -> AppointmentDTO:
        """Obtener cita por ID verificando que pertenece al usuario"""
        appointment = self.appointment_repo.get_by_id(appointment_id)
        if not appointment:
            raise NotFoundException("Cita", appointment_id)
        
        if appointment.user_id != user_id:
            raise BusinessRuleException("No tienes permiso para ver esta cita")
        
        return AppointmentDTO.model_validate(appointment)
    
    def create(self, user_id: int, appointment_data: AppointmentCreateDTO) -> AppointmentDTO:
        """
        Crear una nueva cita
        
        Validaciones:
        - El servicio existe
        - El horario está disponible
        - La fecha es futura
        """
        service = self.service_repo.get_by_id(appointment_data.service_id)
        if not service:
            raise NotFoundException("Servicio", appointment_data.service_id)
        
        if not self.appointment_repo.check_availability(
            appointment_data.appointment_date,
            appointment_data.appointment_time
        ):
            raise BusinessRuleException("El horario seleccionado no está disponible")
        
        new_appointment = Appointment(
            user_id=user_id,
            pet_id=appointment_data.pet_id,
            service_id=appointment_data.service_id,
            appointment_date=appointment_data.appointment_date,
            appointment_time=appointment_data.appointment_time,
            notes=appointment_data.notes,
            estimated_cost=service.price,
            status="pending"
        )
        
        created_appointment = self.appointment_repo.create(new_appointment)
        return AppointmentDTO.model_validate(created_appointment)
    
    def update(self, appointment_id: int, user_id: int, appointment_data: AppointmentUpdateDTO) -> AppointmentDTO:
        """Actualizar una cita existente"""
        appointment = self.appointment_repo.get_by_id(appointment_id)
        if not appointment:
            raise NotFoundException("Cita", appointment_id)
        
        if appointment.user_id != user_id:
            raise BusinessRuleException("No tienes permiso para modificar esta cita")
        
        if (appointment_data.appointment_date or appointment_data.appointment_time):
            new_date = appointment_data.appointment_date or appointment.appointment_date
            new_time = appointment_data.appointment_time or appointment.appointment_time
            
            if (new_date != appointment.appointment_date or new_time != appointment.appointment_time):
                if not self.appointment_repo.check_availability(new_date, new_time):
                    raise BusinessRuleException("El horario seleccionado no está disponible")
        
        if appointment_data.appointment_date:
            appointment.appointment_date = appointment_data.appointment_date
        if appointment_data.appointment_time:
            appointment.appointment_time = appointment_data.appointment_time
        if appointment_data.status:
            appointment.status = appointment_data.status
        if appointment_data.notes is not None:
            appointment.notes = appointment_data.notes
        
        updated_appointment = self.appointment_repo.update(appointment)
        return AppointmentDTO.model_validate(updated_appointment)
    
    def cancel(self, appointment_id: int, user_id: int) -> AppointmentDTO:
        """Cancelar una cita"""
        appointment = self.appointment_repo.get_by_id(appointment_id)
        if not appointment:
            raise NotFoundException("Cita", appointment_id)
        
        if appointment.user_id != user_id:
            raise BusinessRuleException("No tienes permiso para cancelar esta cita")
        
        appointment.status = "cancelled"
        updated_appointment = self.appointment_repo.update(appointment)
        return AppointmentDTO.model_validate(updated_appointment)
