from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    company: Optional[str] = None
    lead_id: Optional[int] = None

class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    company: Optional[str]
    lead_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
