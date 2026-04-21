"""
Usuarios de demostración por rol (login en /api/v1/auth/login).

Ejecutar tras migraciones: python seed_users.py
En Docker se ejecuta automáticamente en docker-entrypoint.sh
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text

from app.core.database import SessionLocal
from app.core.security import get_password_hash

# Credenciales demo (solo desarrollo; cambiar en producción)
DEMO_USERS = [
    {
        "email": "veterinario@demo.vet",
        "name": "Dra. Demo Veterinaria",
        "password": "veterinario123",
        "role": "veterinario",
        "phone": "+51 900 111 001",
        "address": "Clínica Fulness — Panel veterinario",
    },
    {
        "email": "cliente@demo.vet",
        "name": "Cliente Demo",
        "password": "cliente123",
        "role": "user",
        "phone": "+51 900 222 002",
        "address": "Av. Demo 123",
    },
    {
        "email": "admin@demo.vet",
        "name": "Admin Catálogo",
        "password": "admin123",
        "role": "admin",
        "phone": "+51 900 333 003",
        "address": "Oficina central",
    },
]


def seed_users() -> None:
    db = SessionLocal()
    insert_sql = text("""
        INSERT INTO users (email, name, password_hash, role, is_active, phone, address, created_at)
        VALUES (:email, :name, :password, :role, :is_active, :phone, :address, NOW())
    """)
    try:
        print("[seed_users] Comprobando usuarios demo por rol...")
        for u in DEMO_USERS:
            row = db.execute(
                text("SELECT id FROM users WHERE email = :email"),
                {"email": u["email"]},
            ).fetchone()
            if row:
                print(f"  - Ya existe: {u['email']} ({u['role']})")
                continue
            print(f"  + Creando: {u['email']} (rol: {u['role']})")
            db.execute(
                insert_sql,
                {
                    "email": u["email"],
                    "name": u["name"],
                    "password": get_password_hash(u["password"]),
                    "role": u["role"],
                    "is_active": True,
                    "phone": u["phone"],
                    "address": u["address"],
                },
            )
            db.commit()
        print("[seed_users] Listo.")
    except Exception as e:
        print(f"[seed_users] Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_users()
