from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from core.database import get_db
from app import models
from app.repositories import RSVPRepository, OrderRepository
from app.services import OrderService

router = APIRouter()
html_templates = Jinja2Templates(directory="templates")


@router.get("/invitation/{invitation_id}/responses", name="admin_responses")
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


@router.get("/orders", name="admin_orders")
def view_orders(request: Request, db: Session = Depends(get_db)):
    order_service = OrderService(OrderRepository(db))
    orders = order_service.get_all_orders()

    return html_templates.TemplateResponse("admin_orders.html", {
        "request": request,
        "orders": orders
    })