from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.core.database import get_db
from app.infrastructure.database.models.pet import Pet
from app.presentation.dependencies.auth import get_current_user
from app.infrastructure.database.models.user import User

router = APIRouter()


class PetDTO(BaseModel):
    id: int
    name: str
    species: str | None = None
    gender: str | None = None
    breed: str | None = None
    age: int | None = None
    weight: float | None = None

    class Config:
        from_attributes = True


class PetCreateDTO(BaseModel):
    name: str
    species: str | None = None
    gender: str | None = None
    breed: str | None = None
    age: int | None = None
    weight: float | None = None


class PetUpdateDTO(BaseModel):
    name: str | None = None
    species: str | None = None
    gender: str | None = None
    breed: str | None = None
    age: int | None = None
    weight: float | None = None


@router.get("/user/{user_id}", response_model=List[PetDTO])
async def get_pets_by_user(user_id: int, db: Session = Depends(get_db)):
    """Listar mascotas de un usuario (usado por el panel veterinario)."""
    pets = db.query(Pet).filter(Pet.owner_id == user_id).all()
    return pets


@router.post("/", response_model=PetDTO, status_code=status.HTTP_201_CREATED)
async def create_pet(
    body: PetCreateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Registrar mascota del usuario autenticado."""
    pet = Pet(
        owner_id=current_user.id,
        name=body.name,
        species=body.species,
        gender=body.gender,
        breed=body.breed,
        age=body.age,
        weight=Decimal(str(body.weight)) if body.weight is not None else None,
        medical_history=[],
    )
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


@router.patch("/{pet_id}", response_model=PetDTO)
async def update_pet(
    pet_id: int,
    body: PetUpdateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Actualizar datos de la mascota (solo el dueño)."""
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
    if pet.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")

    data = body.model_dump(exclude_unset=True)
    if "weight" in data and data["weight"] is not None:
        data["weight"] = Decimal(str(data["weight"]))
    if "gender" in data and data["gender"] == "":
        data["gender"] = None
    for k, v in data.items():
        setattr(pet, k, v)
    db.commit()
    db.refresh(pet)
    return pet
