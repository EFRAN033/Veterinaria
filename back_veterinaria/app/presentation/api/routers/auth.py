"""
Router de autenticación refactorizado con arquitectura limpia
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.application.services.auth_service import AuthService
from app.application.dtos.user_dto import UserCreateDTO, LoginDTO, UserDTO, TokenDTO
from app.presentation.dependencies.auth import get_current_user
from app.infrastructure.database.models.user import User
from app.core.exceptions import ConflictException, UnauthorizedException, ForbiddenException, ValidationException

router = APIRouter()


@router.post("/register", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreateDTO, db: Session = Depends(get_db)):
    """
    Registrar un nuevo usuario
    """
    try:
        auth_service = AuthService(db)
        return auth_service.register(user_data)
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.post("/login", response_model=TokenDTO)
async def login(credentials: LoginDTO, db: Session = Depends(get_db)):
    """
    Login de usuario y retorno de JWT token
    """
    try:
        auth_service = AuthService(db)
        return auth_service.login(credentials)
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ForbiddenException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)


@router.get("/me", response_model=UserDTO)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Obtener información del usuario autenticado
    """
    return UserDTO.model_validate(current_user)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout():
    """
    Logout de usuario (en JWT stateless no se hace nada en backend, 
    pero el frontend espera este endpoint para limpiar estado)
    """
    return {"message": "Logout exitoso"}
