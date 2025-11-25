from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, ARRAY, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String)
    category = Column(String(50))  # beds, food, toys, clothes, accessories
    price = Column(DECIMAL(10, 2), nullable=False)
    old_price = Column(DECIMAL(10, 2))
    discount = Column(String(10))
    stock = Column(Integer, default=0)
    images = Column(ARRAY(String), default=[])
    rating = Column(DECIMAL(2, 1), default=0)
    reviews = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
