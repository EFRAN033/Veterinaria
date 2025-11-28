from sqlalchemy import Column, Integer, String, ARRAY, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Adoption(Base):
    __tablename__ = "adoptions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    species = Column(String(50))  
    age = Column(String(50))
    description = Column(String)
    images = Column(ARRAY(String), default=[])
    status = Column(String(20), default="available")
    available = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
