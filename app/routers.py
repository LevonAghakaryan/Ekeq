from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from core.database import get_db
from app import models

router = APIRouter()
html_templates = Jinja2Templates(directory="templates")


# 1. Գլխավոր էջ (Home) - ԱՌԱՋԻՆԸ
@router.get("/", name="home")
def home(request: Request):
    return html_templates.TemplateResponse("home.html", {"request": request})


# 2. Կատալոգ - Բոլոր պրոդուկտները
@router.get("/catalog", name="catalog")
def show_catalog(request: Request, db: Session = Depends(get_db)):
    all_products = db.query(models.Template).all()
    return html_templates.TemplateResponse("catalog_new.html", {
        "request": request,
        "templates": all_products
    })


# 3. Պրոդուկտի մանրամասն էջ
@router.get("/product/{product_id}", name="product_detail")
def show_product_detail(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Template).filter(models.Template.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Պրոդուկտը չի գտնվել")

    return html_templates.TemplateResponse("product_detail.html", {
        "request": request,
        "product": product
    })


# 4. Հրավիրատոմսի էջ (slug-ով) - ՎԵՐՋԻՆԸ, որպեսզի չբռնի այլ routes
@router.get("/invite/{slug}", name="invitation")
def show_invitation(request: Request, slug: str, db: Session = Depends(get_db)):
    invitation = db.query(models.Invitation).filter(models.Invitation.slug == slug).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Հրավիրատոմսը չի գտնվել")

    # Վերցնում է template-ի html ֆայլը
    return html_templates.TemplateResponse(f"designs/{invitation.template.html_file}", {
        "request": request,
        "data": invitation
    })