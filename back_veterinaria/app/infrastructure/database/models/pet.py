from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, ARRAY, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Pet(Base):
    __tablename__ = "pets"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    species = Column(String(50)) 
    breed = Column(String(100))
    age = Column(Integer)
    weight = Column(DECIMAL(5, 2))
    medical_history = Column(ARRAY(String), default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    owner = relationship("User", back_populates="pets")
    appointments = relationship("Appointment", back_populates="pet")
