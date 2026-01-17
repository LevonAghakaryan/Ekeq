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


class RSVPRepository(BaseRepository):
    def get_by_invitation_id(self, invitation_id: int):
        """Վերադարձնում է բոլոր responses-ները տվյալ հրավիրատոմսի համար"""
        return self.db.query(models.RSVPResponse).filter(
            models.RSVPResponse.invitation_id == invitation_id
        ).order_by(models.RSVPResponse.submitted_at.desc()).all()

    def create(self, rsvp: schemas.RSVPResponseCreate):
        """Նոր RSVP response ստեղծել"""
        db_rsvp = models.RSVPResponse(**rsvp.model_dump())
        self.db.add(db_rsvp)
        self.db.commit()
        self.db.refresh(db_rsvp)
        return db_rsvp

    def get_stats(self, invitation_id: int):
        """Վիճակագրություն - քանի հոգի գալիս է"""
        responses = self.get_by_invitation_id(invitation_id)

        yes_count = sum(r.guest_count for r in responses if r.attending == "yes")
        no_count = len([r for r in responses if r.attending == "no"])
        maybe_count = sum(r.guest_count for r in responses if r.attending == "maybe")

        return {
            "total_yes": yes_count,
            "total_no": no_count,
            "total_maybe": maybe_count,
            "total_responses": len(responses)
        }