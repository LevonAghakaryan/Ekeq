from pydantic import BaseModel


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