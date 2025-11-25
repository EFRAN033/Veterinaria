"""
DTOs para servicios veterinarios
"""
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class ServiceCreateDTO(BaseModel):
    """DTO para crear un servicio"""
    name: str
    description: Optional[str] = None
    category: str
    price: Decimal
    duration: Optional[int] = None  # en minutos


class ServiceUpdateDTO(BaseModel):
    """DTO para actualizar un servicio"""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Decimal] = None
    duration: Optional[int] = None
    is_active: Optional[bool] = None


class ServiceDTO(BaseModel):
    """DTO para respuesta de servicio"""
    id: int
    name: str
    description: Optional[str] = None
    category: str
    price: Decimal
    duration: Optional[int] = None
    is_active: bool
    
    class Config:
        from_attributes = True
