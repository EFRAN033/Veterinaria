from app.core.database import SessionLocal
from app.infrastructure.database.models.user import User

db = SessionLocal()
try:
    users = db.query(User).all()
    for user in users:
        print(f"User ID: {user.id}, Email: {user.email}, Role: {user.role}")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
