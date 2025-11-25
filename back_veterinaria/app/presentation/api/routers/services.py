"""
Router de servicios veterinarios refactorizado con arquitectura limpia
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.application.services.service_service import ServiceService
from app.application.dtos.service_dto import ServiceCreateDTO, ServiceUpdateDTO, ServiceDTO
from app.presentation.dependencies.auth import get_current_admin_user
from app.infrastructure.database.models.user import User
from app.core.exceptions import NotFoundException, ValidationException

router = APIRouter()


@router.get("/", response_model=List[ServiceDTO])
async def get_services(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    db: Session = Depends(get_db)
):
    """
    Obtener todos los servicios activos
    Opcionalmente filtrar por categoría
    """
    service_service = ServiceService(db)
    
    if category:
        return service_service.get_by_category(category, active_only=True)
    
    return service_service.get_all(skip=skip, limit=limit, active_only=True)


@router.get("/{service_id}", response_model=ServiceDTO)
async def get_service(service_id: int, db: Session = Depends(get_db)):
    """
    Obtener un servicio por ID
    """
    try:
        service_service = ServiceService(db)
        return service_service.get_by_id(service_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.post("/", response_model=ServiceDTO, status_code=status.HTTP_201_CREATED)
async def create_service(
    service_data: ServiceCreateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Crear un nuevo servicio (solo administradores)
    """
    try:
        service_service = ServiceService(db)
        return service_service.create(service_data)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.put("/{service_id}", response_model=ServiceDTO)
async def update_service(
    service_id: int,
    service_data: ServiceUpdateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Actualizar un servicio (solo administradores)
    """
    try:
        service_service = ServiceService(db)
        return service_service.update(service_id, service_data)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Eliminar un servicio (solo administradores)
    """
    try:
        service_service = ServiceService(db)
        service_service.delete(service_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
