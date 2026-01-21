from sqlalchemy.orm import Session
from app import models, schemas


class TemplateRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(models.Template).all()

    def get_by_id(self, template_id: int):
        return self.db.query(models.Template).filter(models.Template.id == template_id).first()

    def create(self, template: schemas.TemplateCreate):
        db_template = models.Template(**template.model_dump())
        self.db.add(db_template)
        self.db.commit()
        self.db.refresh(db_template)
        return db_template