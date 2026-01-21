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
    music_url = Column(String(255), nullable=True)

    invitations = relationship("Invitation", back_populates="template")
    media_files = relationship("TemplateMedia", back_populates="template", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="template")  # ՆՈՐ


class TemplateMedia(Base):
    __tablename__ = "templates_media"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    file_url = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False)  # 'image' կամ 'video'

    template = relationship("Template", back_populates="media_files")


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


class Order(Base):  # ՆՈՐ ԱՂՅՈՒՍԱԿ
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(200), nullable=False)
    phone_number = Column(String(20), nullable=False)
    preferred_contact = Column(String(20), nullable=False)  # 'WhatsApp', 'Telegram', 'Viber', 'Phone'
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    status = Column(String(20), default="New")  # 'New', 'Pending', 'Completed'
    created_at = Column(DateTime, default=datetime.utcnow)

    template = relationship("Template", back_populates="orders")