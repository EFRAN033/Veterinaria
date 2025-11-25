"""
DTOs for Service Requests
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ServiceTypeEnum(str, Enum):
    """Service type enumeration"""
    CONSULTATION = "consultation"
    GENERAL = "general"
    CLINICAL = "clinical"
    AESTHETIC = "aesthetic"


class RequestStatusEnum(str, Enum):
    """Request status enumeration"""
    PENDING = "pending"
    REVIEWED = "reviewed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ServiceRequestCreateDTO(BaseModel):
    """DTO for creating a service request"""
    service_type: ServiceTypeEnum
    pet_name: Optional[str] = None
    estimated_cost: float = Field(ge=0)
    service_data: Dict[str, Any]  # All form fields specific to service type
    images: Optional[List[str]] = []  # Base64 encoded images


class ServiceRequestUpdateDTO(BaseModel):
    """DTO for updating a service request (veterinarian only)"""
    status: Optional[RequestStatusEnum] = None
    assigned_vet_id: Optional[int] = None
    vet_notes: Optional[str] = None


class ServiceRequestDTO(BaseModel):
    """DTO for service request response"""
    id: int
    user_id: int
    service_type: ServiceTypeEnum
    status: RequestStatusEnum
    pet_name: Optional[str]
    estimated_cost: float
    service_data: Dict[str, Any]
    images: Optional[List[str]]
    assigned_vet_id: Optional[int]
    vet_notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    
    class Config:
        from_attributes = True
