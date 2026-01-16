from sqlalchemy.orm import Session
from . import models, schemas

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

class TemplateRepository(BaseRepository):
    def get_all(self):
        return self.db.query(models.Template).all()

    def create(self, template: schemas.TemplateCreate):
        db_template = models.Template(**template.model_dump())
        self.db.add(db_template)
        self.db.commit()
        self.db.refresh(db_template)
        return db_template

class InvitationRepository(BaseRepository):
    def get_by_slug(self, slug: str):
        return self.db.query(models.Invitation).filter(models.Invitation.slug == slug).first()

    def create(self, invitation: schemas.InvitationCreate):
        db_invitation = models.Invitation(**invitation.model_dump())
        self.db.add(db_invitation)
        self.db.commit()
        self.db.refresh(db_invitation)
        return db_invitation