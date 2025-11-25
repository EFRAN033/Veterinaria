"""
Service Request Repository Implementation
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.domain.interfaces.service_request_repository import ServiceRequestRepository
from app.infrastructure.database.models.service_request import ServiceRequest


class ServiceRequestRepositoryImpl(ServiceRequestRepository):
    """Implementation of service request repository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, service_request: ServiceRequest) -> ServiceRequest:
        """Create a new service request"""
        self.db.add(service_request)
        self.db.commit()
        self.db.refresh(service_request)
        # Load user relationship using a fresh query
        return self.get_by_id(service_request.id)
    
    def get_by_id(self, request_id: int) -> Optional[ServiceRequest]:
        """Get service request by ID with user relationship loaded"""
        return self.db.query(ServiceRequest)\
            .options(joinedload(ServiceRequest.user))\
            .options(joinedload(ServiceRequest.assigned_vet))\
            .filter(ServiceRequest.id == request_id)\
            .first()
    
    def get_all(
        self,
        status: Optional[str] = None,
        service_type: Optional[str] = None,
        assigned_vet_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ServiceRequest]:
        """Get all service requests with optional filters"""
        query = self.db.query(ServiceRequest)\
            .options(joinedload(ServiceRequest.user))\
            .options(joinedload(ServiceRequest.assigned_vet))
        
        if status:
            query = query.filter(ServiceRequest.status == status)
        
        if service_type:
            query = query.filter(ServiceRequest.service_type == service_type)
        
        if assigned_vet_id:
            query = query.filter(ServiceRequest.assigned_vet_id == assigned_vet_id)
        
        return query.order_by(ServiceRequest.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_by_user_id(self, user_id: int) -> List[ServiceRequest]:
        """Get all service requests for a specific user"""
        return self.db.query(ServiceRequest)\
            .filter(ServiceRequest.user_id == user_id)\
            .order_by(ServiceRequest.created_at.desc())\
            .all()
    
    def update(self, service_request: ServiceRequest) -> ServiceRequest:
        """Update service request"""
        self.db.commit()
        self.db.refresh(service_request)
        return service_request
    
    def delete(self, request_id: int) -> bool:
        """Delete service request"""
        service_request = self.get_by_id(request_id)
        if service_request:
            self.db.delete(service_request)
            self.db.commit()
            return True
        return False
