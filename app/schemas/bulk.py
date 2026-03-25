from pydantic import BaseModel
from typing import List

class BulkStatusUpdate(BaseModel):
    lead_ids: List[int]
    status: str

class BulkDelete(BaseModel):
    lead_ids: List[int]
