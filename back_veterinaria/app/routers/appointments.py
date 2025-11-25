from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.appointment import Appointment
from app.models.user import User
from app.dependencies.auth import get_current_user
from pydantic import BaseModel
from datetime import date, time

router = APIRouter()

class AppointmentResponse(BaseModel):
    id: int
    user_id: int
    pet_id: Optional[int]
    service_id: Optional[int]
    appointment_date: date
    appointment_time: time
    status: str
    notes: Optional[str]
    estimated_cost: Optional[float]
    
    class Config:
        orm_mode = True

class AppointmentStatusUpdate(BaseModel):
    status: str

def get_current_vet(current_user: User = Depends(get_current_user)):
    if current_user.role != "veterinario":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren privilegios de veterinario"
        )
    return current_user


@router.get("/pending", response_model=List[AppointmentResponse])
async def get_pending_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_vet)
):
    """
    Get all appointments with status 'pending'
    """
    return db.query(Appointment).filter(Appointment.status == "pending").all()

@router.get("/history", response_model=List[AppointmentResponse])
async def get_appointment_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_vet)
):
    """
    Get all appointments with status 'completed' or 'cancelled'
    """
    return db.query(Appointment).filter(Appointment.status.in_(["completed", "cancelled"])).all()

@router.get("/all", response_model=List[AppointmentResponse])
async def get_all_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_vet)
):
    """
    Get all appointments (for calendar view)
    """
    return db.query(Appointment).all()

@router.patch("/{appointment_id}/status", response_model=AppointmentResponse)
async def update_appointment_status(
    appointment_id: int,
    status_update: AppointmentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_vet)
):
    """
    Update the status of an appointment
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    appointment.status = status_update.status
    db.commit()
    db.refresh(appointment)
    return appointment

@router.get("/", response_model=List[AppointmentResponse])
async def get_my_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get appointments for the current user
    """
    if current_user.role == "veterinario":
        return db.query(Appointment).all()
    return db.query(Appointment).filter(Appointment.user_id == current_user.id).all()
