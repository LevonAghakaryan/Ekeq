from app.repositories import TemplateRepository, TemplateMediaRepository


class TemplateService:
    def __init__(self, repo: TemplateRepository, media_repo: TemplateMediaRepository = None):
        self.repo = repo
        self.media_repo = media_repo

    def list_templates(self):
        return self.repo.get_all()

    def get_template_with_media(self, template_id: int):
        template = self.repo.get_by_id(template_id)
        return template if template else None