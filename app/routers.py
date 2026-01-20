from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from core.database import get_db
from app import models, schemas
from app.repositories import RSVPRepository, TemplateMediaRepository
from app.services import RSVPService, TemplateMediaService

router = APIRouter()
html_templates = Jinja2Templates(directory="templates")


# 1. Գլխավոր էջ (Home)
@router.get("/", name="home")
def home(request: Request):
    return html_templates.TemplateResponse("home.html", {"request": request})


# 2. Կատալոգ
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

    # Մեդիա ֆայլերը վերցնել
    media_service = TemplateMediaService(TemplateMediaRepository(db))
    media_files = media_service.get_template_media(product_id)

    return html_templates.TemplateResponse("product_detail.html", {
        "request": request,
        "product": product,
        "media_files": media_files  # ԱՎԵԼԱՑՎԱԾ
    })


# 4. Հրավիրատոմսի էջ (slug-ով)
@router.get("/invite/{slug}", name="invitation")
def show_invitation(request: Request, slug: str, db: Session = Depends(get_db)):
    invitation = db.query(models.Invitation).filter(models.Invitation.slug == slug).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Հրավիրատոմսը չի գտնվել")

    # Վիճակագրություն
    rsvp_repo = RSVPRepository(db)
    stats = rsvp_repo.get_stats(invitation.id)

    # Մեդիա ֆայլերը վերցնել
    media_service = TemplateMediaService(TemplateMediaRepository(db))
    media_files = media_service.get_template_media(invitation.template_id)

    return html_templates.TemplateResponse(f"designs/{invitation.template.html_file}", {
        "request": request,
        "data": invitation,
        "stats": stats,
        "media_files": media_files,  # ԱՎԵԼԱՑՎԱԾ
        "music_url": invitation.template.music_url  # ԱՎԵԼԱՑՎԱԾ
    })


# 5. RSVP Submit (Form POST)
@router.post("/invite/{slug}/rsvp", name="submit_rsvp")
async def submit_rsvp(
        slug: str,
        guest_name: str = Form(...),
        attending: str = Form(...),
        guest_count: int = Form(1),
        message: str = Form(None),
        db: Session = Depends(get_db)
):
    # Invitation գտնել
    invitation = db.query(models.Invitation).filter(models.Invitation.slug == slug).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Հրավիրատոմսը չի գտնվել")

    # RSVP save անել
    rsvp_data = schemas.RSVPResponseCreate(
        invitation_id=invitation.id,
        guest_name=guest_name,
        attending=attending,
        guest_count=guest_count,
        message=message
    )

    rsvp_service = RSVPService(RSVPRepository(db))
    rsvp_service.submit_response(rsvp_data)

    # Redirect դեպի success էջ կամ նույն էջը
    return RedirectResponse(url=f"/invite/{slug}?success=true", status_code=303)


# 6. Admin - Տեսնել responses-ները (optional)
@router.get("/admin/invitation/{invitation_id}/responses", name="admin_responses")
def view_responses(request: Request, invitation_id: int, db: Session = Depends(get_db)):
    invitation = db.query(models.Invitation).filter(models.Invitation.id == invitation_id).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Հրավիրատոմսը չի գտնվել")

    rsvp_repo = RSVPRepository(db)
    responses = rsvp_repo.get_by_invitation_id(invitation_id)
    stats = rsvp_repo.get_stats(invitation_id)

    return html_templates.TemplateResponse("admin_responses.html", {
        "request": request,
        "invitation": invitation,
        "responses": responses,
        "stats": stats
    })