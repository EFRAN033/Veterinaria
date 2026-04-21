from app.application.dtos.appointment_dto import AppointmentDTO
from app.infrastructure.database.models.appointment import Appointment


def appointment_to_dto(appointment: Appointment) -> AppointmentDTO:
    pet = appointment.pet if getattr(appointment, "pet", None) else None
    return AppointmentDTO(
        id=appointment.id,
        user_id=appointment.user_id,
        pet_id=appointment.pet_id,
        service_id=appointment.service_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        status=appointment.status,
        notes=appointment.notes,
        final_diagnosis=getattr(appointment, "final_diagnosis", None),
        treatment=getattr(appointment, "treatment", None),
        estimated_cost=appointment.estimated_cost,
        pet_name=pet.name if pet else None,
        species=pet.species if pet else None,
        gender=getattr(pet, "gender", None) if pet else None,
    )
