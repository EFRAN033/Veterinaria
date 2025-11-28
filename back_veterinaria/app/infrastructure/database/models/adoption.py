from sqlalchemy import Column, Integer, String, ARRAY, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Adoption(Base):
    __tablename__ = "adoptions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    species = Column(String(50)) 
    breed = Column(String(100))
    age = Column(String(50))
    gender = Column(String(20))
    phone = Column(String(50))
    email = Column(String(255))
    description = Column(String)
    images = Column(ARRAY(String), default=[])
    status = Column(String(20), default="available") 
    available = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
