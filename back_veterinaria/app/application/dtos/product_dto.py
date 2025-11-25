"""
DTOs para productos
"""
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class ProductCreateDTO(BaseModel):
    """DTO para crear un producto"""
    name: str
    description: Optional[str] = None
    category: str
    price: Decimal
    stock: int = 0
    image_url: Optional[str] = None


class ProductUpdateDTO(BaseModel):
    """DTO para actualizar un producto"""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class ProductDTO(BaseModel):
    """DTO para respuesta de producto"""
    id: int
    name: str
    description: Optional[str] = None
    category: str
    price: Decimal
    stock: int
    image_url: Optional[str] = None
    is_active: bool
    
    class Config:
        from_attributes = True
