from pydantic import BaseModel


class TemplateMediaBase(BaseModel):
    file_url: str
    file_type: str  # 'image' կամ 'video'


class TemplateMediaCreate(TemplateMediaBase):
    invitation_id: int


class TemplateMedia(TemplateMediaBase):
    id: int
    invitation_id: int

    class Config:
        from_attributes = True