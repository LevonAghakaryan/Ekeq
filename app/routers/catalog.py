from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from core.database import get_db
from app import models

router = APIRouter()
html_templates = Jinja2Templates(directory="templates")


@router.get("/catalog", name="catalog")
def show_catalog(request: Request, db: Session = Depends(get_db)):
    all_products = db.query(models.Template).all()

    # Յուրաքանչյուր template-ի համար ավելացնում ենք preview_image
    for template in all_products:
        # Գտնում ենք առաջին invitation-ը, որը օգտագործում է այս template-ը
        first_invitation = db.query(models.Invitation).filter(
            models.Invitation.template_id == template.id
        ).first()

        # Եթե կա invitation, վերցնում ենք դրա առաջին նկարը որպես preview
        if first_invitation and first_invitation.media_files:
            template.preview_image = first_invitation.media_files[0].file_url
        else:
            template.preview_image = None

    return html_templates.TemplateResponse("catalog_new.html", {
        "request": request,
        "templates": all_products
    })