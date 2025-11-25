"""
Router de usuarios - Placeholder
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.presentation.dependencies.auth import get_current_admin_user
from app.infrastructure.database.models.user import User

router = APIRouter()


@router.get("/")
async def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Obtener todos los usuarios (solo admin)
    TODO: Implementar con arquitectura limpia
    """
    return {"message": "Users endpoint - En desarrollo"}
