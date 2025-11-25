"""
DTOs para citas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date, time
from decimal import Decimal


class AppointmentCreateDTO(BaseModel):
    """DTO para crear una cita"""
    pet_id: Optional[int] = None
    service_id: int
    appointment_date: date
    appointment_time: time
    notes: Optional[str] = None


class AppointmentUpdateDTO(BaseModel):
    """DTO para actualizar una cita"""
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class AppointmentDTO(BaseModel):
    """DTO para respuesta de cita"""
    id: int
    user_id: int
    pet_id: Optional[int] = None
    service_id: int
    appointment_date: date
    appointment_time: time
    status: str
    notes: Optional[str] = None
    estimated_cost: Optional[Decimal] = None
    
    class Config:
        from_attributes = True
