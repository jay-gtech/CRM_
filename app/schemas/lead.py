from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    salutation: Optional[str] = None
    email: EmailStr
    secondary_email: Optional[EmailStr] = None
    phone: str
    skype_id: Optional[str] = None
    twitter: Optional[str] = None
    website: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    rating: Optional[int] = 0
    tag: Optional[str] = None
    status: str = "New"
    source: Optional[str] = None
    owner_id: Optional[int] = None
    lead_score: int = 0
    is_converted: bool = False
    converted_at: Optional[datetime] = None
    last_contacted_at: Optional[datetime] = None
    unsubscribed_mode: Optional[str] = None
    unsubscribed_time: Optional[datetime] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    salutation: Optional[str] = None
    email: Optional[EmailStr] = None
    secondary_email: Optional[EmailStr] = None
    phone: Optional[str] = None
    skype_id: Optional[str] = None
    twitter: Optional[str] = None
    website: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    rating: Optional[int] = None
    tag: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    owner_id: Optional[int] = None
    lead_score: Optional[int] = None
    is_converted: Optional[bool] = None
    converted_at: Optional[datetime] = None
    last_contacted_at: Optional[datetime] = None
    unsubscribed_mode: Optional[str] = None
    unsubscribed_time: Optional[datetime] = None

class LeadResponse(LeadBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
