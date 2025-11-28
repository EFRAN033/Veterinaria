from sqlalchemy import create_engine, text
from app.core.config import settings

# Database connection
engine = create_engine(settings.DATABASE_URL)

def clear_database():
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            # Disable triggers to avoid foreign key constraints issues during deletion if needed, 
            # but usually cascading delete handles it. 
            # However, to be safe and thorough, we delete in order.
            
            print("Deleting Service Requests...")
            connection.execute(text("DELETE FROM service_requests"))
            
            print("Deleting Appointments...")
            connection.execute(text("DELETE FROM appointments"))
            
            print("Deleting Pets...")
            connection.execute(text("DELETE FROM pets"))
            
            print("Deleting Users (except admin/vet if needed, but user said 'delete all')...")
            # User said "borrame los clientes y mascotas", implying maybe keep the vet?
            # "veterinario@test.com" is the one logged in. We should probably keep him.
            connection.execute(text("DELETE FROM users WHERE email != 'veterinario@test.com'"))
            
            trans.commit()
            print("Database cleared successfully!")
        except Exception as e:
            trans.rollback()
            print(f"Error clearing database: {e}")

if __name__ == "__main__":
    clear_database()
