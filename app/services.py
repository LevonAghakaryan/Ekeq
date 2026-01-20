from .repositories import TemplateRepository, TemplateMediaRepository, InvitationRepository, RSVPRepository


class TemplateService:
    def __init__(self, repo: TemplateRepository, media_repo: TemplateMediaRepository = None):
        self.repo = repo
        self.media_repo = media_repo

    def list_templates(self):
        return self.repo.get_all()

    def get_template_with_media(self, template_id: int):
        """Template-ը վերադարձնել բոլոր մեդիա ֆայլերով"""
        template = self.repo.get_by_id(template_id)
        if not template:
            return None

        # Եթե media_repo տրված է, ապա media-ն ավտոմատ կլինի relationship-ի շնորհիվ
        return template


class TemplateMediaService:
    def __init__(self, repo: TemplateMediaRepository):
        self.repo = repo

    def add_media_to_template(self, template_id: int, file_url: str, file_type: str):
        """Մեկ մեդիա ֆայլ ավելացնել"""
        from app import schemas
        media_data = schemas.TemplateMediaCreate(
            template_id=template_id,
            file_url=file_url,
            file_type=file_type
        )
        return self.repo.create(media_data)

    def add_multiple_media(self, template_id: int, media_files: list):
        """Բազմաթիվ մեդիա ֆայլեր ավելացնել միանգամից"""
        from app import schemas
        media_list = [
            schemas.TemplateMediaCreate(
                template_id=template_id,
                file_url=media['file_url'],
                file_type=media['file_type']
            )
            for media in media_files
        ]
        return self.repo.create_multiple(media_list)

    def get_template_media(self, template_id: int):
        """Վերադարձնել բոլոր մեդիան"""
        return self.repo.get_by_template_id(template_id)


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