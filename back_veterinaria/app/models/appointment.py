from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    pet_id = Column(Integer, ForeignKey("pets.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    status = Column(String(20), default="pending")  # pending, confirmed, completed, cancelled
    notes = Column(String)
    estimated_cost = Column(DECIMAL(10, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="appointments")
    pet = relationship("Pet", back_populates="appointments")
