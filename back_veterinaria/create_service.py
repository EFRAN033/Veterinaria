from app.core.database import SessionLocal
from app.infrastructure.database.models.service import Service

db = SessionLocal()
try:
    service = Service(
        name="Consulta General",
        description="Consulta veterinaria básica",
        category="consultation",
        price=50.00,
        duration=30,
        is_active=True
    )
    db.add(service)
    db.commit()
    print(f"Service created with ID: {service.id}")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
