from pydantic import BaseModel
from typing import List, Optional

# Template Schemas
class TemplateBase(BaseModel):
    name: str
    html_file: str
    price: float

class TemplateCreate(TemplateBase):
    pass

class Template(TemplateBase):
    id: int
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