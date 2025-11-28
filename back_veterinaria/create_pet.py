from app.core.database import SessionLocal
from app.infrastructure.database.models.pet import Pet

db = SessionLocal()
try:
    pet = Pet(
        name="Max",
        species="Perro",
        breed="Labrador",
        age=5,
        weight=30.0,
        owner_id=1
    )
    db.add(pet)
    db.commit()
    print(f"Pet created with ID: {pet.id}")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
