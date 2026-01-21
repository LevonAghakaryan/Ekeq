from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(200), nullable=False)
    phone_number = Column(String(20), nullable=False)
    preferred_contact = Column(String(20), nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    status = Column(String(20), default="New")
    created_at = Column(DateTime, default=datetime.utcnow)

    template = relationship("Template", back_populates="orders")