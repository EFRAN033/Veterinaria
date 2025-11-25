"""
Implementación del repositorio de usuarios
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.infrastructure.database.models.user import User
from app.core.exceptions import NotFoundException


class UserRepositoryImpl:
    """Implementación concreta del repositorio de usuarios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Obtener todos los usuarios con paginación"""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def create(self, user: User) -> User:
        """Crear un nuevo usuario"""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user: User) -> User:
        """Actualizar un usuario existente"""
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        """Eliminar un usuario"""
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
    
    def exists_by_email(self, email: str) -> bool:
        """Verificar si existe un usuario con el email dado"""
        return self.db.query(User).filter(User.email == email).first() is not None
