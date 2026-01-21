from sqlalchemy.orm import Session
from app import models, schemas


class InvitationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_slug(self, slug: str):
        return self.db.query(models.Invitation).filter(models.Invitation.slug == slug).first()

    def create(self, invitation: schemas.InvitationCreate):
        db_invitation = models.Invitation(**invitation.model_dump())
        self.db.add(db_invitation)
        self.db.commit()
        self.db.refresh(db_invitation)
        return db_invitation