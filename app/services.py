from .repositories import TemplateRepository, InvitationRepository

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