from sqlalchemy.orm import Session
from . import models, schemas


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db


class TemplateRepository(BaseRepository):
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


class TemplateMediaRepository(BaseRepository):
    def get_by_template_id(self, template_id: int):
        """Վերադարձնում է բոլոր մեդիա ֆայլերը տվյալ Template-ի համար"""
        return self.db.query(models.TemplateMedia).filter(
            models.TemplateMedia.template_id == template_id
        ).all()

    def create(self, media: schemas.TemplateMediaCreate):
        """Նոր մեդիա ֆայլ ստեղծել"""
        db_media = models.TemplateMedia(**media.model_dump())
        self.db.add(db_media)
        self.db.commit()
        self.db.refresh(db_media)
        return db_media

    def create_multiple(self, media_list: list):
        """Բազմաթիվ մեդիա ֆայլեր միանգամից ավելացնել"""
        db_media_list = [models.TemplateMedia(**media.model_dump()) for media in media_list]
        self.db.add_all(db_media_list)
        self.db.commit()
        return db_media_list

    def delete_by_template_id(self, template_id: int):
        """Ջնջել բոլոր մեդիան տվյալ Template-ից"""
        self.db.query(models.TemplateMedia).filter(
            models.TemplateMedia.template_id == template_id
        ).delete()
        self.db.commit()


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


class OrderRepository(BaseRepository):  # ՆՈՐ REPOSITORY
    def create(self, order: schemas.OrderCreate):
        """Նոր պատվեր ստեղծել"""
        db_order = models.Order(**order.model_dump())
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def get_all(self):
        """Բոլոր պատվերները վերադարձնել"""
        return self.db.query(models.Order).order_by(models.Order.created_at.desc()).all()

    def get_by_id(self, order_id: int):
        """Պատվերը ID-ով գտնել"""
        return self.db.query(models.Order).filter(models.Order.id == order_id).first()

    def update_status(self, order_id: int, new_status: str):
        """Պատվերի կարգավիճակը թարմացնել"""
        order = self.get_by_id(order_id)
        if order:
            order.status = new_status
            self.db.commit()
            self.db.refresh(order)
        return order