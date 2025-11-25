"""
Router de adopciones - Placeholder
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()


@router.get("/")
async def get_adoptions(db: Session = Depends(get_db)):
    """
    Obtener mascotas en adopción
    TODO: Implementar con arquitectura limpia
    """
    return {"message": "Adoptions endpoint - En desarrollo"}
