from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    company = Column(String)
    status = Column(String, default="New") # New, Contacted, Qualified, Lost
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    deals = relationship("Deal", back_populates="lead", foreign_keys="Deal.lead_id")
