from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.db.base_class import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    company = Column(String)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
