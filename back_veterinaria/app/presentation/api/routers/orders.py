"""
Router de órdenes - Placeholder
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.presentation.dependencies.auth import get_current_user
from app.infrastructure.database.models.user import User

router = APIRouter()


@router.get("/")
async def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener órdenes del usuario
    TODO: Implementar con arquitectura limpia
    """
    return {"message": "Orders endpoint - En desarrollo", "user_id": current_user.id}
