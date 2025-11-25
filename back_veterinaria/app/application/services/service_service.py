"""
Servicio de gestión de servicios veterinarios
Contiene la lógica de negocio para CRUD de servicios
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from decimal import Decimal
from app.application.dtos.service_dto import ServiceCreateDTO, ServiceUpdateDTO, ServiceDTO
from app.infrastructure.repositories.service_repository_impl import ServiceRepositoryImpl
from app.infrastructure.database.models.service import Service
from app.core.exceptions import NotFoundException, ValidationException


class ServiceService:
    """Servicio de gestión de servicios veterinarios"""
    
    def __init__(self, db: Session):
        self.db = db
        self.service_repo = ServiceRepositoryImpl(db)
    
    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[ServiceDTO]:
        """Obtener todos los servicios"""
        services = self.service_repo.get_all(skip=skip, limit=limit, active_only=active_only)
        return [ServiceDTO.model_validate(service) for service in services]
    
    def get_by_id(self, service_id: int) -> ServiceDTO:
        """Obtener servicio por ID"""
        service = self.service_repo.get_by_id(service_id)
        if not service:
            raise NotFoundException("Servicio", service_id)
        return ServiceDTO.model_validate(service)
    
    def get_by_category(self, category: str, active_only: bool = True) -> List[ServiceDTO]:
        """Obtener servicios por categoría"""
        services = self.service_repo.get_by_category(category, active_only=active_only)
        return [ServiceDTO.model_validate(service) for service in services]
    
    def create(self, service_data: ServiceCreateDTO) -> ServiceDTO:
        """
        Crear un nuevo servicio
        
        Validaciones:
        - Precio mayor a 0
        - Duración mayor a 0 si se proporciona
        """
        if service_data.price <= 0:
            raise ValidationException("El precio debe ser mayor a 0", field="price")
        
        if service_data.duration is not None and service_data.duration <= 0:
            raise ValidationException("La duración debe ser mayor a 0", field="duration")
        
        new_service = Service(
            name=service_data.name,
            description=service_data.description,
            category=service_data.category,
            price=service_data.price,
            duration=service_data.duration
        )
        
        created_service = self.service_repo.create(new_service)
        return ServiceDTO.model_validate(created_service)
    
    def update(self, service_id: int, service_data: ServiceUpdateDTO) -> ServiceDTO:
        """Actualizar un servicio existente"""
        service = self.service_repo.get_by_id(service_id)
        if not service:
            raise NotFoundException("Servicio", service_id)
        
        if service_data.price is not None and service_data.price <= 0:
            raise ValidationException("El precio debe ser mayor a 0", field="price")
        
        if service_data.duration is not None and service_data.duration <= 0:
            raise ValidationException("La duración debe ser mayor a 0", field="duration")
        
        if service_data.name is not None:
            service.name = service_data.name
        if service_data.description is not None:
            service.description = service_data.description
        if service_data.category is not None:
            service.category = service_data.category
        if service_data.price is not None:
            service.price = service_data.price
        if service_data.duration is not None:
            service.duration = service_data.duration
        if service_data.is_active is not None:
            service.is_active = service_data.is_active
        
        updated_service = self.service_repo.update(service)
        return ServiceDTO.model_validate(updated_service)
    
    def delete(self, service_id: int) -> bool:
        """Eliminar un servicio"""
        service = self.service_repo.get_by_id(service_id)
        if not service:
            raise NotFoundException("Servicio", service_id)
        
        return self.service_repo.delete(service_id)
