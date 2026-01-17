from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    html_file = Column(String(100), nullable=False)
    price = Column(Float, default=0.0)

    invitations = relationship("Invitation", back_populates="template")


class Invitation(Base):
    __tablename__ = "invitations"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True)
    event_title = Column(String(200))
    template_id = Column(Integer, ForeignKey("templates.id"))

    template = relationship("Template", back_populates="invitations")
    responses = relationship("RSVPResponse", back_populates="invitation")


class RSVPResponse(Base):
    __tablename__ = "rsvp_responses"

    id = Column(Integer, primary_key=True, index=True)
    invitation_id = Column(Integer, ForeignKey("invitations.id"), nullable=False)
    guest_name = Column(String(200), nullable=False)
    attending = Column(String(10), nullable=False)  # 'yes', 'no', 'maybe'
    guest_count = Column(Integer, default=1)
    message = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    invitation = relationship("Invitation", back_populates="responses")