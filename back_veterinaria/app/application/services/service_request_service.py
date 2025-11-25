"""
Service Request Service
Business logic for service requests
"""
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from app.application.dtos.service_request_dto import (
    ServiceRequestCreateDTO,
    ServiceRequestUpdateDTO,
    ServiceRequestDTO,
    ServiceTypeEnum,
    RequestStatusEnum
)
from app.infrastructure.repositories.service_request_repository_impl import ServiceRequestRepositoryImpl
from app.infrastructure.database.models.service_request import ServiceRequest, ServiceType, RequestStatus
from app.core.file_storage import save_base64_images, delete_images
from app.core.exceptions import NotFoundException, ValidationException, ForbiddenException

logger = logging.getLogger(__name__)


class ServiceRequestService:
    """Service for managing service requests"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repo = ServiceRequestRepositoryImpl(db)
    
    def create_service_request(self, user_id: int, request_data: ServiceRequestCreateDTO) -> ServiceRequestDTO:
        """
        Create a new service request
        
        Args:
            user_id: ID of the user creating the request
            request_data: Service request data
            
        Returns:
            Created service request
        """
        logger.info(f"Creating service request for user {user_id}, type: {request_data.service_type}")
        
        # Validate service data based on type
        self._validate_service_data(request_data.service_type, request_data.service_data)
        
        # Save images if provided
        image_paths = []
        if request_data.images:
            try:
                image_paths = save_base64_images(request_data.images, user_id)
                logger.info(f"Saved {len(image_paths)} images for service request")
            except Exception as e:
                logger.error(f"Error saving images: {e}")
                raise ValidationException(f"Error al guardar imágenes: {str(e)}")
        
        # Create service request
        service_request = ServiceRequest(
            user_id=user_id,
            service_type=request_data.service_type.value,  # Use string value directly
            status="pending",  # Use string value directly
            pet_name=request_data.pet_name,
            estimated_cost=request_data.estimated_cost,
            service_data=request_data.service_data,
            images=image_paths
        )
        
        created_request = self.repo.create(service_request)
        logger.info(f"Service request created with ID: {created_request.id}")
        
        return self._to_dto(created_request)
    
    def get_service_request(self, request_id: int) -> ServiceRequestDTO:
        """Get service request by ID"""
        service_request = self.repo.get_by_id(request_id)
        if not service_request:
            raise NotFoundException(f"Service request {request_id} not found")
        
        return self._to_dto(service_request)
    
    def get_all_service_requests(
        self,
        status: Optional[RequestStatusEnum] = None,
        service_type: Optional[ServiceTypeEnum] = None,
        assigned_vet_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ServiceRequestDTO]:
        """Get all service requests with optional filters (for veterinarians)"""
        status_filter = status.value if status else None
        type_filter = service_type.value if service_type else None
        
        requests = self.repo.get_all(
            status=status_filter,
            service_type=type_filter,
            assigned_vet_id=assigned_vet_id,
            skip=skip,
            limit=limit
        )
        
        return [self._to_dto(req) for req in requests]
    
    def get_user_service_requests(self, user_id: int) -> List[ServiceRequestDTO]:
        """Get all service requests for a specific user"""
        requests = self.repo.get_by_user_id(user_id)
        return [self._to_dto(req) for req in requests]
    
    def update_service_request(
        self,
        request_id: int,
        update_data: ServiceRequestUpdateDTO,
        user_id: int,
        user_role: str
    ) -> ServiceRequestDTO:
        """
        Update service request (veterinarian only)
        
        Args:
            request_id: ID of the request to update
            update_data: Update data
            user_id: ID of the user making the update
            user_role: Role of the user
            
        Returns:
            Updated service request
        """
        # Only veterinarians can update requests
        if user_role != "veterinario":
            raise ForbiddenException("Only veterinarians can update service requests")
        
        service_request = self.repo.get_by_id(request_id)
        if not service_request:
            raise NotFoundException(f"Service request {request_id} not found")
        
        # Update fields
        if update_data.status:
            service_request.status = update_data.status.value  # Use string value directly
        
        if update_data.assigned_vet_id is not None:
            service_request.assigned_vet_id = update_data.assigned_vet_id
        
        if update_data.vet_notes is not None:
            service_request.vet_notes = update_data.vet_notes
        
        updated_request = self.repo.update(service_request)
        logger.info(f"Service request {request_id} updated by user {user_id}")
        
        return self._to_dto(updated_request)
    
    def _validate_service_data(self, service_type: ServiceTypeEnum, service_data: dict):
        """Validate service data based on service type"""
        required_fields = {
            ServiceTypeEnum.CONSULTATION: ['species', 'symptoms', 'urgency'],
            ServiceTypeEnum.GENERAL: ['serviceType'],
            ServiceTypeEnum.CLINICAL: ['description'],
            ServiceTypeEnum.AESTHETIC: ['species', 'services']
        }
        
        required = required_fields.get(service_type, [])
        missing = [field for field in required if field not in service_data or not service_data[field]]
        
        if missing:
            raise ValidationException(f"Missing required fields: {', '.join(missing)}")
    
    def _to_dto(self, service_request: ServiceRequest) -> ServiceRequestDTO:
        """Convert ServiceRequest model to DTO"""
        dto_data = {
            "id": service_request.id,
            "user_id": service_request.user_id,
            "service_type": ServiceTypeEnum(service_request.service_type),
            "status": RequestStatusEnum(service_request.status),
            "pet_name": service_request.pet_name,
            "estimated_cost": float(service_request.estimated_cost) if service_request.estimated_cost else 0.0,
            "service_data": service_request.service_data or {},
            "images": service_request.images or [],
            "assigned_vet_id": service_request.assigned_vet_id,
            "vet_notes": service_request.vet_notes,
            "created_at": service_request.created_at,
            "updated_at": service_request.updated_at
        }
        
        # Add user info if available
        if service_request.user:
            dto_data["user_name"] = service_request.user.name
            dto_data["user_email"] = service_request.user.email
        
        return ServiceRequestDTO(**dto_data)
