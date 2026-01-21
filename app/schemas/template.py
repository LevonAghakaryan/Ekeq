from pydantic import BaseModel
from typing import List, Optional


class TemplateBase(BaseModel):
    name: str
    html_file: str
    price: float
    music_url: Optional[str] = None


class TemplateCreate(TemplateBase):
    pass


class Template(TemplateBase):
    id: int

    class Config:
        from_attributes = True