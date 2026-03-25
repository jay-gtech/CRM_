from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class LeadCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    company: Optional[str] = None
    status: str = "New"

class LeadUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None

class LeadResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    company: Optional[str]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
