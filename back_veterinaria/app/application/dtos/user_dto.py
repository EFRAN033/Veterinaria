"""
DTOs para usuarios
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreateDTO(BaseModel):
    """DTO para crear un usuario"""
    email: EmailStr
    name: str
    password: str
    phone: Optional[str] = None
    address: Optional[str] = None


class UserUpdateDTO(BaseModel):
    """DTO para actualizar un usuario"""
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class UserDTO(BaseModel):
    """DTO para respuesta de usuario"""
    id: int
    email: str
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class LoginDTO(BaseModel):
    """DTO para login"""
    email: EmailStr
    password: str


class TokenDTO(BaseModel):
    """DTO para token de acceso"""
    access_token: str
    token_type: str = "bearer"
