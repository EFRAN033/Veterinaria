import sys
import os
from sqlalchemy import text

# Add parent directory to path to allow imports from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.core.security import get_password_hash

def seed_users():
    db = SessionLocal()
    try:
        print("Checking for initial users...")

        # 1. Create Veterinarian
        vet_email = "veterinario@admin.com"
        vet = db.execute(text("SELECT * FROM users WHERE email = :email"), {"email": vet_email}).fetchone()
        
        if not vet:
            print(f"Creating Veterinarian ({vet_email})...")
            db.execute(text("""
                INSERT INTO users (email, name, password_hash, role, is_active, phone, address, created_at) 
                VALUES (:email, :name, :password, :role, :is_active, :phone, :address, NOW())
            """), {
                "email": vet_email,
                "name": "Admin Veterinario",
                "password": get_password_hash("admin123"),
                "role": "veterinario",
                "is_active": True,
                "phone": "555-0001",
                "address": "Clínica Principal"
            })
            db.commit()
            print("✅ Veterinarian created.")
        else:
            print(f"ℹ️ Veterinarian already exists.")

        # 2. Create Client
        client_email = "cliente@usuario.com"
        client = db.execute(text("SELECT * FROM users WHERE email = :email"), {"email": client_email}).fetchone()
        
        if not client:
            print(f"Creating Client ({client_email})...")
            db.execute(text("""
                INSERT INTO users (email, name, password_hash, role, is_active, phone, address, created_at) 
                VALUES (:email, :name, :password, :role, :is_active, :phone, :address, NOW())
            """), {
                "email": client_email,
                "name": "Usuario Cliente",
                "password": get_password_hash("cliente123"),
                "role": "user",
                "is_active": True,
                "phone": "555-0002",
                "address": "Calle 123"
            })
            db.commit()
            print("✅ Client created.")
        else:
            print(f"ℹ️ Client already exists.")

    except Exception as e:
        print(f"❌ Error seeding users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()
