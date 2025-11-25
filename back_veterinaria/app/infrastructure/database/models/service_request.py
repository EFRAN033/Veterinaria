"""
Service Request Model
Stores service requests from clients with all details and images
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON, DECIMAL, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class ServiceType(str, enum.Enum):
    """Service type enumeration"""
    CONSULTATION = "consultation"
    GENERAL = "general"
    CLINICAL = "clinical"
    AESTHETIC = "aesthetic"


class RequestStatus(str, enum.Enum):
    """Request status enumeration"""
    PENDING = "pending"
    REVIEWED = "reviewed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ServiceRequest(Base):
    """Service Request model for storing client service requests"""
    __tablename__ = "service_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    service_type = Column(String(20), nullable=False)  # Store enum value as string
    status = Column(String(20), default="pending")  # Store enum value as string
    
    pet_name = Column(String(100))
    estimated_cost = Column(DECIMAL(10, 2))
    
    service_data = Column(JSON)
    
    images = Column(JSON)  # ["uploads/service_requests/1/image1.jpg", ...]
    
    assigned_vet_id = Column(Integer, ForeignKey("users.id"))
    vet_notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", foreign_keys=[user_id], back_populates="service_requests")
    assigned_vet = relationship("User", foreign_keys=[assigned_vet_id])
