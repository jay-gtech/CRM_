from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActivityCreate(BaseModel):
    activity_type: str # Call, Email, Task
    description: str
    lead_id: Optional[int] = None
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None

class ActivityResponse(BaseModel):
    id: int
    activity_type: str
    description: str
    lead_id: Optional[int]
    contact_id: Optional[int]
    deal_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
