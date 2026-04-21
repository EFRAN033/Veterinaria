"""DTOs para panel veterinario (analíticas)."""

from pydantic import BaseModel, Field


class VetMonthCountDTO(BaseModel):
    month: str = Field(..., description="Primer día del mes en ISO (YYYY-MM-DD)")
    count: int


class VetStatusCountDTO(BaseModel):
    status: str
    count: int


class VetAnalyticsDTO(BaseModel):
    appointments_by_month: list[VetMonthCountDTO]
    appointments_by_status: list[VetStatusCountDTO]
    total_appointments: int
    unique_pets_attended: int
    follow_up_patients_count: int
    follow_up_legend: str = (
        "Mascotas distintas con al menos una cita futura en estado pendiente o confirmada."
    )
    range_months: int
