from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AccountBase(BaseModel):
    name: str
    website: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None

class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountBase):
    name: Optional[str] = None

class AccountResponse(AccountBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
