"""
Implementación del repositorio de servicios
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.infrastructure.database.models.service import Service


class ServiceRepositoryImpl:
    """Implementación concreta del repositorio de servicios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, service_id: int) -> Optional[Service]:
        """Obtener servicio por ID"""
        return self.db.query(Service).filter(Service.id == service_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Service]:
        """Obtener todos los servicios con paginación"""
        query = self.db.query(Service)
        if active_only:
            query = query.filter(Service.is_active == True)
        return query.offset(skip).limit(limit).all()
    
    def get_by_category(self, category: str, active_only: bool = True) -> List[Service]:
        """Obtener servicios por categoría"""
        query = self.db.query(Service).filter(Service.category == category)
        if active_only:
            query = query.filter(Service.is_active == True)
        return query.all()
    
    def create(self, service: Service) -> Service:
        """Crear un nuevo servicio"""
        self.db.add(service)
        self.db.commit()
        self.db.refresh(service)
        return service
    
    def update(self, service: Service) -> Service:
        """Actualizar un servicio existente"""
        self.db.commit()
        self.db.refresh(service)
        return service
    
    def delete(self, service_id: int) -> bool:
        """Eliminar un servicio"""
        service = self.get_by_id(service_id)
        if service:
            self.db.delete(service)
            self.db.commit()
            return True
        return False
