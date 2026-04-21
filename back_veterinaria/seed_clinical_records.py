import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.appointment import Appointment
from app.models.pet import Pet
from app.models.service import Service
from app.core.config import settings

# Database setup
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def seed_clinical_records():
    print("Starting clinical records seeding...")

    # Fetch dependencies
    pets = db.query(Pet).all()
    services = db.query(Service).all()

    if not pets:
        print("❌ No pets found. Please create pets first.")
        return
    if not services:
        print("❌ No services found. Please create services first.")
        return

    # Data pools
    statuses = ['completed', 'completed', 'completed', 'pending', 'cancelled', 'no_show']
    
    diagnoses_pool = [
        "Chequeo de rutina: Todo en orden.",
        "Vacunación anual completada.",
        "Infección leve de oído (Otitis). Se recetaron gotas.",
        "Problemas digestivos: Diarrea leve. Dieta blanda recomendada.",
        "Corte de uñas y limpieza general.",
        "Alergia estacional: Picazón en patas. Antihistamínicos recetados.",
        "Fractura menor en pata trasera. Vendaje aplicado.",
        "Desparasitación interna y externa realizada.",
        "Limpieza dental: Sarro removido.",
        "Conjuntivitis: Ojos rojos. Gotas oftálmicas aplicadas.",
        "Herida superficial por juego brusco. Desinfección realizada.",
        "Chequeo geriátrico: Artrosis detectada. Suplementos recomendados.",
        "Ingestión de cuerpo extraño. Observación requerida.",
        "Tos de las perreras. Aislamiento y medicación.",
        "Sobrepeso detectado. Plan de dieta iniciado.",
        "Revisión post-cirugía: Cicatrización normal.",
        "Problemas de piel: Dermatitis. Champú medicado.",
        "Control de peso: Progreso positivo.",
        "Vacuna antirrábica aplicada.",
        "Consulta por ansiedad. Pautas de comportamiento dadas."
    ]

    records_to_create = 100
    created_count = 0

    for _ in range(records_to_create):
        # Random selection
        pet = random.choice(pets)
        service = random.choice(services)
        status = random.choice(statuses)
        notes = random.choice(diagnoses_pool)
        
        # Random date in last 365 days
        days_ago = random.randint(0, 365)
        random_date = datetime.now() - timedelta(days=days_ago)
        
        # Random time between 9 AM and 6 PM
        hour = random.randint(9, 18)
        minute = random.choice([0, 15, 30, 45])
        appointment_time = random_date.replace(hour=hour, minute=minute, second=0).time()

        # Create appointment
        appointment = Appointment(
            user_id=pet.owner_id,
            pet_id=pet.id,
            service_id=service.id,
            appointment_date=random_date.date(),
            appointment_time=appointment_time,
            status=status,
            notes=notes,
            estimated_cost=service.price,
            created_at=random_date
        )
        
        db.add(appointment)
        created_count += 1

    try:
        db.commit()
        print(f"✅ Successfully created {created_count} clinical records.")
    except Exception as e:
        print(f"❌ Error saving records: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_clinical_records()
