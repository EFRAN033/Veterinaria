"""Rutas exclusivas del rol veterinario (analíticas)."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.application.services.appointment_service import AppointmentService
from app.application.dtos.vet_dto import VetAnalyticsDTO
from app.presentation.dependencies.auth import get_current_veterinario_user
from app.infrastructure.database.models.user import User

router = APIRouter()


@router.get("/analytics", response_model=VetAnalyticsDTO)
async def get_vet_analytics(
    species: str | None = Query(None, description="perro, gato o vacío para todas"),
    sex: str | None = Query(None, description="macho, hembra o vacío para todos"),
    range_months: int = Query(12, ge=1, le=36),
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_veterinario_user),
):
    svc = AppointmentService(db)
    return svc.get_vet_analytics(species=species, sex=sex, range_months=range_months)
