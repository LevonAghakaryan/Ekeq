from app.repositories import RSVPRepository


class RSVPService:
    def __init__(self, repo: RSVPRepository):
        self.repo = repo

    def submit_response(self, rsvp_data):
        return self.repo.create(rsvp_data)

    def get_invitation_responses(self, invitation_id: int):
        return self.repo.get_by_invitation_id(invitation_id)

    def get_invitation_stats(self, invitation_id: int):
        return self.repo.get_stats(invitation_id)