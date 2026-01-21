from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RSVPResponseBase(BaseModel):
    guest_name: str
    attending: str  # 'yes', 'no', 'maybe'
    guest_count: int = 1
    message: Optional[str] = None


class RSVPResponseCreate(RSVPResponseBase):
    invitation_id: int


class RSVPResponse(RSVPResponseBase):
    id: int
    invitation_id: int
    submitted_at: datetime

    class Config:
        from_attributes = True