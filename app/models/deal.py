from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.db.base_class import Base

class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    amount = Column(Float, default=0.0)
    stage = Column(String, default="New") # New, Contacted, Qualified, Negotiation, Won, Lost
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
