from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from core.database import Base


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    html_file = Column(String(100), nullable=False)
    price = Column(Float, default=0.0)
    music_url = Column(String(255), nullable=True)

    invitations = relationship("Invitation", back_populates="template")
    orders = relationship("Order", back_populates="template")