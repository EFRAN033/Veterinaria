"""
Interfaz del repositorio de servicios
"""
from typing import Protocol, Optional, List
from app.infrastructure.database.models.service import Service


class ServiceRepository(Protocol):
    """Protocolo que define las operaciones del repositorio de servicios"""
    
    def get_by_id(self, service_id: int) -> Optional[Service]:
        """Obtener servicio por ID"""
        ...
    
    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Service]:
        """Obtener todos los servicios con paginación"""
        ...
    
    def get_by_category(self, category: str, active_only: bool = True) -> List[Service]:
        """Obtener servicios por categoría"""
        ...
    
    def create(self, service: Service) -> Service:
        """Crear un nuevo servicio"""
        ...
    
    def update(self, service: Service) -> Service:
        """Actualizar un servicio existente"""
        ...
    
    def delete(self, service_id: int) -> bool:
        """Eliminar un servicio"""
        ...
