from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.db.base_class import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    activity_type = Column(String) # Call, Email, Task, Meeting
    subject = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(String, default="Pending") # Pending, Completed (for Tasks)
    priority = Column(String, default="Medium") # Low, Medium, High
    due_date = Column(DateTime, nullable=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
