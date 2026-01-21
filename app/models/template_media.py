from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class TemplateMedia(Base):
    __tablename__ = "templates_media"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    file_url = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False)  # 'image' կամ 'video'

    template = relationship("Template", back_populates="media_files")