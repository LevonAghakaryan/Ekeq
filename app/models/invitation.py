from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True)
    event_title = Column(String(200))
    template_id = Column(Integer, ForeignKey("templates.id"))

    template = relationship("Template", back_populates="invitations")
    responses = relationship("RSVPResponse", back_populates="invitation", cascade="all, delete-orphan")
    media_files = relationship("TemplateMedia", back_populates="invitation", cascade="all, delete-orphan")