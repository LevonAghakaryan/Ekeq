from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# TemplateMedia Schemas
class TemplateMediaBase(BaseModel):
    file_url: str
    file_type: str  # 'image' կամ 'video'


class TemplateMediaCreate(TemplateMediaBase):
    template_id: int


class TemplateMedia(TemplateMediaBase):
    id: int
    template_id: int

    class Config:
        from_attributes = True


# Template Schemas
class TemplateBase(BaseModel):
    name: str
    html_file: str
    price: float
    music_url: Optional[str] = None


class TemplateCreate(TemplateBase):
    pass


class Template(TemplateBase):
    id: int
    media_files: List[TemplateMedia] = []

    class Config:
        from_attributes = True


# Invitation Schemas
class InvitationBase(BaseModel):
    slug: str
    event_title: str
    template_id: int


class InvitationCreate(InvitationBase):
    pass


class Invitation(InvitationBase):
    id: int

    class Config:
        from_attributes = True


# RSVP Schemas
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


# Order Schemas (ՆՈՐ)
class OrderBase(BaseModel):
    customer_name: str
    phone_number: str
    preferred_contact: str  # 'WhatsApp', 'Telegram', 'Viber', 'Phone'
    template_id: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    status: str  # 'New', 'Pending', 'Completed'
    created_at: datetime

    class Config:
        from_attributes = True