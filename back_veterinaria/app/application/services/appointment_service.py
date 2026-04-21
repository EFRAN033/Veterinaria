"""
Servicio de gestión de citas
Contiene la lógica de negocio para CRUD de citas con validaciones
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date, time, datetime
from app.application.dtos.appointment_dto import (
    AppointmentCreateDTO,
    AppointmentUpdateDTO,
    AppointmentDTO,
    AppointmentClinicalUpdateDTO,
)
from app.application.dtos.vet_dto import VetAnalyticsDTO, VetMonthCountDTO, VetStatusCountDTO
from app.application.mappers.appointment_mapper import appointment_to_dto
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
        return [appointment_to_dto(appointment) for appointment in appointments]

    def get_all_appointments(self, skip: int = 0, limit: int = 100) -> List[AppointmentDTO]:
        """Obtener todas las citas (para veterinarios)"""
        appointments = self.appointment_repo.get_all(skip=skip, limit=limit)
        return [appointment_to_dto(appointment) for appointment in appointments]

    def get_vet_history(
        self,
        skip: int = 0,
        limit: int = 100,
        species: Optional[str] = None,
        sex: Optional[str] = None,
    ) -> List[AppointmentDTO]:
        """Historial de citas para veterinario (todas las mascotas/pacientes)."""
        appointments = self.appointment_repo.get_vet_history(
            skip=skip, limit=limit, species=species, sex=sex
        )
        return [appointment_to_dto(a) for a in appointments]

    def get_vet_analytics(
        self,
        species: Optional[str] = None,
        sex: Optional[str] = None,
        range_months: int = 12,
    ) -> VetAnalyticsDTO:
        month_rows, status_rows, total, unique_pets, follow_up = (
            self.appointment_repo.get_analytics_aggregates(
                species=species, sex=sex, range_months=range_months
            )
        )
        by_month: List[VetMonthCountDTO] = []
        for m, c in month_rows:
            if m is None:
                continue
            if isinstance(m, datetime):
                d = m.date()
            else:
                d = m
            by_month.append(VetMonthCountDTO(month=d.isoformat(), count=int(c)))
        by_status = [VetStatusCountDTO(status=s, count=int(cnt)) for s, cnt in status_rows]
        return VetAnalyticsDTO(
            appointments_by_month=by_month,
            appointments_by_status=by_status,
            total_appointments=total,
            unique_pets_attended=unique_pets,
            follow_up_patients_count=follow_up,
            range_months=range_months,
        )
    
    def get_history_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[AppointmentDTO]:
        """Obtener historial de citas (completadas, canceladas o pasadas)"""
        appointments = self.appointment_repo.get_by_user(user_id, skip=0, limit=1000)
        
        history = [
            app for app in appointments 
            if app.status in ["completed", "cancelled"] or 
            (app.appointment_date < date.today() and app.status != "cancelled")
        ]
        
        return [appointment_to_dto(app) for app in history[skip : skip + limit]]

    def get_pending_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[AppointmentDTO]:
        """Obtener citas pendientes (futuras y no canceladas)"""
        appointments = self.appointment_repo.get_by_user(user_id, skip=0, limit=1000)
        
        pending = [
            app for app in appointments 
            if app.status in ["pending", "confirmed"] and app.appointment_date >= date.today()
        ]
        
        return [appointment_to_dto(app) for app in pending[skip : skip + limit]]
    
    def get_by_id(self, appointment_id: int, user_id: int) -> AppointmentDTO:
        """Obtener cita por ID (dueño o veterinario)."""
        appointment = self.appointment_repo.get_by_id(appointment_id)
        if not appointment:
            raise NotFoundException("Cita", appointment_id)

        from app.infrastructure.database.models.user import User

        user = self.db.query(User).filter(User.id == user_id).first()
        is_vet = user.role == "veterinario" if user else False

        if appointment.user_id != user_id and not is_vet:
            raise BusinessRuleException("No tienes permiso para ver esta cita")

        return appointment_to_dto(appointment)
    
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
        
        final_user_id = appointment_data.user_id if appointment_data.user_id else user_id

        new_appointment = Appointment(
            user_id=final_user_id,
            pet_id=appointment_data.pet_id,
            service_id=appointment_data.service_id,
            appointment_date=appointment_data.appointment_date,
            appointment_time=appointment_data.appointment_time,
            notes=appointment_data.notes,
            estimated_cost=service.price,
            status="pending"
        )
        
        created_appointment = self.appointment_repo.create(new_appointment)
        created_appointment = self.appointment_repo.get_by_id(created_appointment.id)
        return appointment_to_dto(created_appointment)
    
    def update(self, appointment_id: int, user_id: int, appointment_data: AppointmentUpdateDTO) -> AppointmentDTO:
        """Actualizar una cita existente"""
        appointment = self.appointment_repo.get_by_id(appointment_id)
        if not appointment:
            raise NotFoundException("Cita", appointment_id)
        
        from app.infrastructure.database.models.user import User
        user = self.db.query(User).filter(User.id == user_id).first()
        is_vet = user.role == "veterinario" if user else False

        if appointment.user_id != user_id and not is_vet:
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
        refreshed = self.appointment_repo.get_by_id(updated_appointment.id)
        return appointment_to_dto(refreshed)

    def update_clinical(
        self,
        appointment_id: int,
        user_id: int,
        data: AppointmentClinicalUpdateDTO,
    ) -> AppointmentDTO:
        """Actualizar diagnóstico final y tratamiento (solo veterinario)."""
        from app.infrastructure.database.models.user import User

        user = self.db.query(User).filter(User.id == user_id).first()
        if not user or user.role != "veterinario":
            raise BusinessRuleException("Solo los veterinarios pueden editar el registro clínico")

        appointment = self.appointment_repo.get_by_id(appointment_id)
        if not appointment:
            raise NotFoundException("Cita", appointment_id)

        if data.final_diagnosis is not None:
            appointment.final_diagnosis = data.final_diagnosis
        if data.treatment is not None:
            appointment.treatment = data.treatment

        self.appointment_repo.update(appointment)
        refreshed = self.appointment_repo.get_by_id(appointment_id)
        return appointment_to_dto(refreshed)

    def cancel(self, appointment_id: int, user_id: int) -> AppointmentDTO:
        """Cancelar una cita"""
        appointment = self.appointment_repo.get_by_id(appointment_id)
        if not appointment:
            raise NotFoundException("Cita", appointment_id)
        
        from app.infrastructure.database.models.user import User
        user = self.db.query(User).filter(User.id == user_id).first()
        is_vet = user.role == "veterinario" if user else False

        if appointment.user_id != user_id and not is_vet:
            raise BusinessRuleException("No tienes permiso para cancelar esta cita")
        
        appointment.status = "cancelled"
        updated_appointment = self.appointment_repo.update(appointment)
        refreshed = self.appointment_repo.get_by_id(updated_appointment.id)
        return appointment_to_dto(refreshed)
