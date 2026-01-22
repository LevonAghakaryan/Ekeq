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


@router.get("/invite/{slug}", name="invitation")
def show_invitation(request: Request, slug: str, db: Session = Depends(get_db)):
    invitation = db.query(models.Invitation).filter(models.Invitation.slug == slug).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Հրավիրատոմսը չի գտնվել")

    rsvp_repo = RSVPRepository(db)
    stats = rsvp_repo.get_stats(invitation.id)

    media_service = TemplateMediaService(TemplateMediaRepository(db))
    media_files = media_service.get_invitation_media(invitation.id)

    return html_templates.TemplateResponse(f"designs/{invitation.template.html_file}", {
        "request": request,
        "data": invitation,
        "stats": stats,
        "media_files": media_files,
        "music_url": invitation.template.music_url
    })


@router.post("/invite/{slug}/rsvp", name="submit_rsvp")
async def submit_rsvp(
        slug: str,
        guest_name: str = Form(...),
        attending: str = Form(...),
        guest_count: int = Form(1),
        message: str = Form(None),
        db: Session = Depends(get_db)
):
    invitation = db.query(models.Invitation).filter(models.Invitation.slug == slug).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Հրավիրատոմսը չի գտնվել")

    rsvp_data = schemas.RSVPResponseCreate(
        invitation_id=invitation.id,
        guest_name=guest_name,
        attending=attending,
        guest_count=guest_count,
        message=message
    )

    rsvp_service = RSVPService(RSVPRepository(db))
    rsvp_service.submit_response(rsvp_data)

    return RedirectResponse(url=f"/invite/{slug}?success=true", status_code=303)