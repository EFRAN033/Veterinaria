"""
Interfaz del repositorio de usuarios
Define el contrato que debe cumplir cualquier implementación del repositorio
"""
from typing import Protocol, Optional, List
from app.infrastructure.database.models.user import User


class UserRepository(Protocol):
    """Protocolo que define las operaciones del repositorio de usuarios"""
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        ...
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        ...
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Obtener todos los usuarios con paginación"""
        ...
    
    def create(self, user: User) -> User:
        """Crear un nuevo usuario"""
        ...
    
    def update(self, user: User) -> User:
        """Actualizar un usuario existente"""
        ...
    
    def delete(self, user_id: int) -> bool:
        """Eliminar un usuario"""
        ...
    
    def exists_by_email(self, email: str) -> bool:
        """Verificar si existe un usuario con el email dado"""
        ...
