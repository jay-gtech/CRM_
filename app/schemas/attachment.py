from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AttachmentBase(BaseModel):
    filename: str
    file_path: str
    file_type: Optional[str] = None
    lead_id: Optional[int] = None
    contact_id: Optional[int] = None

class AttachmentCreate(AttachmentBase):
    pass

class AttachmentResponse(AttachmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
