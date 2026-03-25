from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActivityCreate(BaseModel):
    activity_type: str # Call, Email, Task, Meeting
    subject: Optional[str] = None
    description: Optional[str] = None
    status: str = "Pending"
    priority: str = "Medium"
    due_date: Optional[datetime] = None
    lead_id: Optional[int] = None
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None

class ActivityResponse(BaseModel):
    id: int
    activity_type: str
    subject: Optional[str]
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    lead_id: Optional[int]
    contact_id: Optional[int]
    deal_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
