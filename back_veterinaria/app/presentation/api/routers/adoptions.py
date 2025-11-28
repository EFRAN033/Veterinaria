from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.application.services.adoption_service import AdoptionService
from app.application.dtos.adoption_dto import AdoptionCreate, AdoptionResponse

router = APIRouter()

@router.post("/", response_model=AdoptionResponse)
async def create_adoption(adoption: AdoptionCreate, db: Session = Depends(get_db)):
    """
    Registrar una nueva mascota para adopción
    """
    service = AdoptionService(db)
    return service.create_adoption(adoption)

@router.get("/", response_model=List[AdoptionResponse])
async def get_adoptions(db: Session = Depends(get_db)):
    """
    Obtener todas las mascotas disponibles para adopción
    """
    service = AdoptionService(db)
    return service.get_all_adoptions()
