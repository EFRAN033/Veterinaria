"""
Excepciones personalizadas para la aplicación
"""
from typing import Any, Optional


class DomainException(Exception):
    """Excepción base para errores de dominio"""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class NotFoundException(DomainException):
    """Excepción cuando un recurso no es encontrado"""
    
    def __init__(self, resource: str, identifier: Any):
        message = f"{resource} con identificador '{identifier}' no encontrado"
        super().__init__(message, {"resource": resource, "identifier": identifier})


class ConflictException(DomainException):
    """Excepción cuando hay un conflicto de datos"""
    
    def __init__(self, message: str, field: Optional[str] = None):
        details = {"field": field} if field else None
        super().__init__(message, details)


class UnauthorizedException(DomainException):
    """Excepción cuando la autenticación falla"""
    
    def __init__(self, message: str = "No autorizado"):
        super().__init__(message)


class ForbiddenException(DomainException):
    """Excepción cuando el usuario no tiene permisos"""
    
    def __init__(self, message: str = "No tienes permisos para realizar esta acción"):
        super().__init__(message)


class ValidationException(DomainException):
    """Excepción para errores de validación de negocio"""
    
    def __init__(self, message: str, field: Optional[str] = None):
        details = {"field": field} if field else None
        super().__init__(message, details)


class BusinessRuleException(DomainException):
    """Excepción cuando se viola una regla de negocio"""
    
    def __init__(self, message: str):
        super().__init__(message)
