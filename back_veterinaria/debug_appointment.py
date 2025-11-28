from app.core.database import SessionLocal
from app.application.services.appointment_service import AppointmentService
from app.application.dtos.appointment_dto import AppointmentCreateDTO
from datetime import date, time

db = SessionLocal()
try:
    service = AppointmentService(db)
    dto = AppointmentCreateDTO(
        pet_id=1,
        service_id=1,
        appointment_date=date(2025, 12, 1),
        appointment_time=time(9, 0),
        notes="Debug appointment"
    )
    # user_id 1 is usually the vet or a user. Let's use 1.
    result = service.create(user_id=1, appointment_data=dto)
    print(f"Success: {result}")
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
