"""
Router de citas refactorizado con arquitectura limpia
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.application.services.appointment_service import AppointmentService
from app.application.dtos.appointment_dto import AppointmentCreateDTO, AppointmentUpdateDTO, AppointmentDTO
from app.presentation.dependencies.auth import get_current_user
from app.infrastructure.database.models.user import User
from app.core.exceptions import NotFoundException, ValidationException, BusinessRuleException

router = APIRouter()


@router.get("/", response_model=List[AppointmentDTO])
async def get_appointments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener todas las citas del usuario autenticado
    """
    appointment_service = AppointmentService(db)
    return appointment_service.get_by_user(current_user.id, skip=skip, limit=limit)


@router.get("/{appointment_id}", response_model=AppointmentDTO)
async def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener una cita por ID
    """
    try:
        appointment_service = AppointmentService(db)
        return appointment_service.get_by_id(appointment_id, current_user.id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)


@router.post("/", response_model=AppointmentDTO, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment_data: AppointmentCreateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crear una nueva cita
    """
    try:
        appointment_service = AppointmentService(db)
        return appointment_service.create(current_user.id, appointment_data)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.put("/{appointment_id}", response_model=AppointmentDTO)
async def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentUpdateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar una cita
    """
    try:
        appointment_service = AppointmentService(db)
        return appointment_service.update(appointment_id, current_user.id, appointment_data)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)


@router.delete("/{appointment_id}", response_model=AppointmentDTO)
async def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cancelar una cita
    """
    try:
        appointment_service = AppointmentService(db)
        return appointment_service.cancel(appointment_id, current_user.id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BusinessRuleException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
