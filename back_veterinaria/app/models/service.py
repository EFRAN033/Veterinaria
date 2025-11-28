from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String)
    category = Column(String(50)) 
    price = Column(DECIMAL(10, 2), nullable=False)
    duration = Column(Integer) 
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
