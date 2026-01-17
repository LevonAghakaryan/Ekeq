from .repositories import TemplateRepository, InvitationRepository, RSVPRepository


class TemplateService:
    def __init__(self, repo: TemplateRepository):
        self.repo = repo

    def list_templates(self):
        return self.repo.get_all()


class InvitationService:
    def __init__(self, repo: InvitationRepository):
        self.repo = repo

    def get_invitation_page(self, slug: str):
        invitation = self.repo.get_by_slug(slug)
        if not invitation:
            return None
        return invitation


class RSVPService:
    def __init__(self, repo: RSVPRepository):
        self.repo = repo

    def submit_response(self, rsvp_data):
        """Հյուրի response-ը save անել"""
        return self.repo.create(rsvp_data)

    def get_invitation_responses(self, invitation_id: int):
        """Վերադարձնել բոլոր responses-ները"""
        return self.repo.get_by_invitation_id(invitation_id)

    def get_invitation_stats(self, invitation_id: int):
        """Վիճակագրություն"""
        return self.repo.get_stats(invitation_id)