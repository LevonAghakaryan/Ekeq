from app.repositories import InvitationRepository


class InvitationService:
    def __init__(self, repo: InvitationRepository):
        self.repo = repo

    def get_invitation_page(self, slug: str):
        invitation = self.repo.get_by_slug(slug)
        return invitation if invitation else None