from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DealCreate(BaseModel):
    name: str
    amount: float
    stage: str = "New" # New, Contacted, Qualified, Negotiation, Won, Lost
    contact_id: int

class DealUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    stage: Optional[str] = None
    contact_id: Optional[int] = None

class DealResponse(BaseModel):
    id: int
    name: str
    amount: float
    stage: str
    contact_id: int
    created_at: datetime

    class Config:
        orm_mode = True
