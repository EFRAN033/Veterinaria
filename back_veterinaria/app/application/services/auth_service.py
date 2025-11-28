import logging
from typing import Optional
from sqlalchemy.orm import Session
from app.application.dtos.user_dto import UserCreateDTO, UserDTO, LoginDTO, TokenDTO
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.database.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import ConflictException, UnauthorizedException, ForbiddenException, ValidationException

logger = logging.getLogger(__name__)


class AuthService:
    """Servicio de autenticación y gestión de usuarios"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepositoryImpl(db)
    
    def register(self, user_data: UserCreateDTO) -> UserDTO:
        """
        Registrar un nuevo usuario
        
        Validaciones:
        - Email único
        - Contraseña con mínimo 6 caracteres
        """
        if self.user_repo.exists_by_email(user_data.email):
            raise ConflictException("Este email ya está registrado", field="email")
        
        if len(user_data.password) < 6:
            raise ValidationException("La contraseña debe tener al menos 6 caracteres", field="password")
        
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            name=user_data.name,
            phone=user_data.phone,
            address=user_data.address,
            password_hash=hashed_password,
            role="user"
        )
        
        created_user = self.user_repo.create(new_user)
        return UserDTO.model_validate(created_user)
    
    def login(self, credentials: LoginDTO) -> TokenDTO:
        """
        Autenticar usuario y generar token JWT
        
        Validaciones:
        - Usuario existe
        - Contraseña correcta
        - Usuario activo
        """
        logger.info(f"Intento de login para email: {credentials.email}")
        
        user = self.user_repo.get_by_email(credentials.email)
        
        if not user:
            logger.warning(f"Login fallido: Usuario no encontrado - {credentials.email}")
            raise UnauthorizedException("Email o contraseña incorrectos")
        
        logger.info(f"Usuario encontrado: {user.name} (role: {user.role}, active: {user.is_active})")
        
        if not verify_password(credentials.password, user.password_hash):
            logger.warning(f"Login fallido: Contraseña incorrecta para {credentials.email}")
            raise UnauthorizedException("Email o contraseña incorrectos")
        
        logger.info(f"Contraseña verificada correctamente para {credentials.email}")
        
        if not user.is_active:
            logger.warning(f"Login fallido: Usuario inactivo - {credentials.email}")
            raise ForbiddenException("Usuario inactivo")
        
        access_token = create_access_token(data={
            "sub": user.email,
            "name": user.name,
            "role": user.role
        })
        
        logger.info(f"Login exitoso para {credentials.email} (role: {user.role})")
        
        return TokenDTO(access_token=access_token, token_type="bearer")
    
    def get_current_user(self, email: str) -> Optional[UserDTO]:
        """Obtener usuario actual por email"""
        user = self.user_repo.get_by_email(email)
        if user:
            return UserDTO.model_validate(user)
        return None
