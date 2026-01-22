from sqlalchemy.orm import Session
from app import models, schemas


class TemplateMediaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_invitation_id(self, invitation_id: int):
        return self.db.query(models.TemplateMedia).filter(
            models.TemplateMedia.invitation_id == invitation_id
        ).all()

    def create(self, media: schemas.TemplateMediaCreate):
        db_media = models.TemplateMedia(**media.model_dump())
        self.db.add(db_media)
        self.db.commit()
        self.db.refresh(db_media)
        return db_media

    def create_multiple(self, media_list: list):
        db_media_list = [models.TemplateMedia(**media.model_dump()) for media in media_list]
        self.db.add_all(db_media_list)
        self.db.commit()
        return db_media_list

    def delete_by_invitation_id(self, invitation_id: int):
        self.db.query(models.TemplateMedia).filter(
            models.TemplateMedia.invitation_id == invitation_id
        ).delete()
        self.db.commit()