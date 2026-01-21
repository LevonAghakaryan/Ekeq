from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


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