from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    salutation = Column(String, nullable=True) # Mr, Ms, etc.
    email = Column(String, unique=True, index=True)
    secondary_email = Column(String, nullable=True)
    phone = Column(String, unique=True, index=True)
    skype_id = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
    website = Column(String, nullable=True)
    company = Column(String)
    title = Column(String, nullable=True)
    source = Column(String, nullable=True) # LinkedIn, Website, etc.
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    lead_score = Column(Integer, default=0)
    status = Column(String, default="New") # New, Contacted, Qualified, Lost
    is_converted = Column(Boolean, default=False)
    converted_at = Column(DateTime, nullable=True)
    last_contacted_at = Column(DateTime, nullable=True)
    rating = Column(Integer, default=0) # 1-5
    tag = Column(String, nullable=True)
    unsubscribed_mode = Column(String, nullable=True)
    unsubscribed_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", backref="leads")
