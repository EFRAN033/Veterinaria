"""
Service Requests API Router
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.application.services.service_request_service import ServiceRequestService
from app.application.dtos.service_request_dto import (
    ServiceRequestCreateDTO,
    ServiceRequestUpdateDTO,
    ServiceRequestDTO,
    ServiceTypeEnum,
    RequestStatusEnum
)
from app.presentation.dependencies.auth import get_current_user
from app.infrastructure.database.models.user import User
from app.core.exceptions import NotFoundException, ValidationException, ForbiddenException

router = APIRouter()


@router.post("/", response_model=ServiceRequestDTO, status_code=status.HTTP_201_CREATED)
async def create_service_request(
    request_data: ServiceRequestCreateDTO,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new service request
    
    Requires authentication
    """
    import logging
    import traceback
    logger = logging.getLogger(__name__)
    
    try:
        service = ServiceRequestService(db)
        result = service.create_service_request(current_user.id, request_data)
        logger.info(f"Successfully created service request ID: {result.id}")
        return result
    except ValidationException as e:
        logger.error(f"Validation error: {e.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        logger.error(f"Error creating service request: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[ServiceRequestDTO])
async def get_all_service_requests(
    status_filter: Optional[RequestStatusEnum] = Query(None, alias="status"),
    service_type: Optional[ServiceTypeEnum] = Query(None, alias="service_type"),
    assigned_vet_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all service requests (veterinarians only)
    
    Supports filtering by status, service type, and assigned veterinarian
    """
    # Only veterinarians can view all requests
    if current_user.role != "veterinario":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only veterinarians can view all service requests"
        )
    
    service = ServiceRequestService(db)
    return service.get_all_service_requests(
        status=status_filter,
        service_type=service_type,
        assigned_vet_id=assigned_vet_id,
        skip=skip,
        limit=limit
    )


@router.get("/my-requests", response_model=List[ServiceRequestDTO])
async def get_my_service_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all service requests for the current user
    
    Requires authentication
    """
    service = ServiceRequestService(db)
    return service.get_user_service_requests(current_user.id)


@router.get("/{request_id}", response_model=ServiceRequestDTO)
async def get_service_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific service request by ID
    
    Users can only view their own requests, veterinarians can view all
    """
    try:
        service = ServiceRequestService(db)
        service_request = service.get_service_request(request_id)
        
        # Check permissions
        if current_user.role != "veterinario" and service_request.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own service requests"
            )
        
        return service_request
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.patch("/{request_id}", response_model=ServiceRequestDTO)
async def update_service_request(
    request_id: int,
    update_data: ServiceRequestUpdateDTO,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a service request (veterinarians only)
    
    Allows updating status, assigned veterinarian, and vet notes
    """
    try:
        service = ServiceRequestService(db)
        return service.update_service_request(
            request_id=request_id,
            update_data=update_data,
            user_id=current_user.id,
            user_role=current_user.role
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
