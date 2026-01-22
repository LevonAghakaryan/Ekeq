from app.repositories import TemplateMediaRepository
from app import schemas


class TemplateMediaService:
    def __init__(self, repo: TemplateMediaRepository):
        self.repo = repo

    def add_media_to_invitation(self, invitation_id: int, file_url: str, file_type: str):
        media_data = schemas.TemplateMediaCreate(
            invitation_id=invitation_id,
            file_url=file_url,
            file_type=file_type
        )
        return self.repo.create(media_data)

    def add_multiple_media(self, invitation_id: int, media_files: list):
        media_list = [
            schemas.TemplateMediaCreate(
                invitation_id=invitation_id,
                file_url=media['file_url'],
                file_type=media['file_type']
            )
            for media in media_files
        ]
        return self.repo.create_multiple(media_list)

    def get_invitation_media(self, invitation_id: int):
        return self.repo.get_by_invitation_id(invitation_id)