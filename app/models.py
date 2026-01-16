from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from core.database import Base


# app/models.py

class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    html_file = Column(String(100), nullable=False)
    price = Column(Float, default=0.0)

    # Ուղղված է՝ back_populates
    invitations = relationship("Invitation", back_populates="template")


class Invitation(Base):
    __tablename__ = "invitations"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True)
    event_title = Column(String(200))
    template_id = Column(Integer, ForeignKey("templates.id"))

    # Ուղղված է՝ back_populates
    template = relationship("Template", back_populates="invitations")