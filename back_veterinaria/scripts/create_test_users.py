import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to sys.path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.infrastructure.database.models.user import User
from app.core.security import get_password_hash

def create_test_users():
    print(f"Connecting to database: {settings.SQLALCHEMY_DATABASE_URI}")
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # 1. Create Regular User
        user_email = "usuario@test.com"
        existing_user = db.query(User).filter(User.email == user_email).first()
        if not existing_user:
            print(f"Creating regular user: {user_email}")
            user = User(
                name="Usuario Prueba",
                email=user_email,
                password_hash=get_password_hash("usuario123"),
                phone="999888777",
                address="Av. Prueba 123",
                role="user",
                is_active=True
            )
            db.add(user)
            print("Regular user created successfully.")
        else:
            print(f"User {user_email} already exists.")

        # 2. Create Veterinarian User
        vet_email = "veterinario@test.com"
        existing_vet = db.query(User).filter(User.email == vet_email).first()
        if not existing_vet:
            print(f"Creating veterinarian user: {vet_email}")
            vet = User(
                name="Dr. Veterinario Prueba",
                email=vet_email,
                password_hash=get_password_hash("veterinario123"),
                phone="999111222",
                address="Clínica Veterinaria",
                role="veterinario",
                is_active=True
            )
            db.add(vet)
            print("Veterinarian user created successfully.")
        else:
            print(f"User {vet_email} already exists.")

        db.commit()
        print("\n✅ Test users setup complete!")
        print(f"User: {user_email} / usuario123")
        print(f"Vet:  {vet_email} / veterinario123")

    except Exception as e:
        print(f"❌ Error creating users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_users()
