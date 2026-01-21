from sqlalchemy.orm import Session
from app import models, schemas


class RSVPRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_invitation_id(self, invitation_id: int):
        return self.db.query(models.RSVPResponse).filter(
            models.RSVPResponse.invitation_id == invitation_id
        ).order_by(models.RSVPResponse.submitted_at.desc()).all()

    def create(self, rsvp: schemas.RSVPResponseCreate):
        db_rsvp = models.RSVPResponse(**rsvp.model_dump())
        self.db.add(db_rsvp)
        self.db.commit()
        self.db.refresh(db_rsvp)
        return db_rsvp

    def get_stats(self, invitation_id: int):
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