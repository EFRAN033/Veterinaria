from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AdoptionBase(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    age: str
    gender: str
    phone: str
    email: Optional[str] = None
    description: Optional[str] = None
    images: List[str] = []

class AdoptionCreate(AdoptionBase):
    pass

class AdoptionResponse(AdoptionBase):
    id: int
    status: str
    available: int
    created_at: datetime

    class Config:
        from_attributes = True
