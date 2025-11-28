from app.core.database import SessionLocal
from app.infrastructure.database.models.pet import Pet

db = SessionLocal()
try:
    pets = db.query(Pet).all()
    for pet in pets:
        print(f"Pet ID: {pet.id}, Name: {pet.name}, Owner ID: {pet.owner_id}")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
