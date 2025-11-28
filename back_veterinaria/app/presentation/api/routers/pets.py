from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.infrastructure.database.models.pet import Pet
from pydantic import BaseModel

router = APIRouter()

class PetDTO(BaseModel):
    id: int
    name: str
    species: str
    breed: str | None
    age: int | None
    weight: float | None
    
    class Config:
        from_attributes = True

@router.get("/user/{user_id}", response_model=List[PetDTO])
async def get_pets_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get all pets for a specific user
    """
    pets = db.query(Pet).filter(Pet.owner_id == user_id).all()
    return pets
