from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from core.database import get_db
from app import models

router = APIRouter()
html_templates = Jinja2Templates(directory="templates")


# 1. Ցույց տալ բոլոր պրոդուկտները (Catalog)
@router.get("/catalog")
def show_catalog(request: Request, db: Session = Depends(get_db)):
    all_products = db.query(models.Template).all()
    return html_templates.TemplateResponse("catalog.html", {"request": request, "templates": all_products})


# 2. Ցույց տալ կոնկրետ հրավիրատոմսը (Invitation)
@router.get("/{slug}")
def show_invitation(request: Request, slug: str, db: Session = Depends(get_db)):
    invitation = db.query(models.Invitation).filter(models.Invitation.slug == slug).first()
    if not invitation:
        return {"error": "Հրավիրատոմսը չի գտնվել"}

    # Այստեղ համակարգը վերցնում է template-ի մեջ գրված html ֆայլի անունը
    return html_templates.TemplateResponse(f"designs/{invitation.template.html_file}", {
        "request": request,
        "data": invitation
    })