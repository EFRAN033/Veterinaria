#!/usr/bin/env python3
"""
Script to reset user passwords for testing
"""
from app.core.database import SessionLocal
from app.infrastructure.database.models.user import User
from app.core.security import get_password_hash

def reset_passwords():
    db = SessionLocal()
    try:
        # Update veterinarian password
        vet_email = 'vet@veterinaria.com'
        vet_user = db.query(User).filter(User.email == vet_email).first()

        if vet_user:
            vet_user.password_hash = get_password_hash('vet123')
            db.commit()
            print(f'✅ Contraseña actualizada para {vet_email}')
            print(f'   Nueva contraseña: vet123')
        else:
            # Create if doesn't exist
            vet_user = User(
                email=vet_email,
                name='Dr. Veterinario',
                password_hash=get_password_hash('vet123'),
                role='veterinario',
                is_active=True
            )
            db.add(vet_user)
            db.commit()
            print(f'✅ Usuario veterinario creado: {vet_email}')
            print(f'   Contraseña: vet123')

        # Update or create regular user
        user_email = 'cliente@test.com'
        regular_user = db.query(User).filter(User.email == user_email).first()

        if regular_user:
            regular_user.password_hash = get_password_hash('cliente123')
            db.commit()
            print(f'✅ Contraseña actualizada para {user_email}')
            print(f'   Nueva contraseña: cliente123')
        else:
            regular_user = User(
                email=user_email,
                name='Juan Pérez',
                password_hash=get_password_hash('cliente123'),
                role='user',
                is_active=True
            )
            db.add(regular_user)
            db.commit()
            print(f'✅ Usuario cliente creado: {user_email}')
            print(f'   Contraseña: cliente123')

        print()
        print('=' * 50)
        print('CREDENCIALES ACTUALIZADAS')
        print('=' * 50)
        print('VETERINARIO:')
        print('  Email: vet@veterinaria.com')
        print('  Password: vet123')
        print('  Redirect: /veterinario')
        print()
        print('CLIENTE:')
        print('  Email: cliente@test.com')
        print('  Password: cliente123')
        print('  Redirect: /home')
        print('=' * 50)

    except Exception as e:
        print(f'❌ Error: {e}')
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    reset_passwords()
