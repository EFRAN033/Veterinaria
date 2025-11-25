"""
Service Request Repository Interface
"""
from typing import List, Optional
from abc import ABC, abstractmethod
from app.infrastructure.database.models.service_request import ServiceRequest


class ServiceRequestRepository(ABC):
    """Interface for service request repository"""
    
    @abstractmethod
    def create(self, service_request: ServiceRequest) -> ServiceRequest:
        """Create a new service request"""
        pass
    
    @abstractmethod
    def get_by_id(self, request_id: int) -> Optional[ServiceRequest]:
        """Get service request by ID"""
        pass
    
    @abstractmethod
    def get_all(
        self,
        status: Optional[str] = None,
        service_type: Optional[str] = None,
        assigned_vet_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ServiceRequest]:
        """Get all service requests with optional filters"""
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[ServiceRequest]:
        """Get all service requests for a specific user"""
        pass
    
    @abstractmethod
    def update(self, service_request: ServiceRequest) -> ServiceRequest:
        """Update service request"""
        pass
    
    @abstractmethod
    def delete(self, request_id: int) -> bool:
        """Delete service request"""
        pass
