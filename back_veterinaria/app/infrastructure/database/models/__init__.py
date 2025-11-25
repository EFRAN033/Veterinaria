# Import all models here for Alembic to detect them
from app.infrastructure.database.models.user import User
from app.infrastructure.database.models.pet import Pet
from app.infrastructure.database.models.service import Service
from app.infrastructure.database.models.appointment import Appointment
from app.infrastructure.database.models.product import Product
from app.infrastructure.database.models.order import Order, OrderItem
from app.infrastructure.database.models.adoption import Adoption

__all__ = [
    "User",
    "Pet",
    "Service",
    "Appointment",
    "Product",
    "Order",
    "OrderItem",
    "Adoption"
]
