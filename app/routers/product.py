from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from core.database import get_db
from app import models, schemas
from app.repositories import TemplateMediaRepository, OrderRepository
from app.services import TemplateMediaService, OrderService

router = APIRouter()
html_templates = Jinja2Templates(directory="templates")


@router.get("/product/{product_id}", name="product_detail")
def show_product_detail(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Template).filter(models.Template.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Պրոդուկտը չի գտնվել")

    media_service = TemplateMediaService(TemplateMediaRepository(db))
    media_files = media_service.get_template_media(product_id)

    return html_templates.TemplateResponse("product_detail.html", {
        "request": request,
        "product": product,
        "media_files": media_files
    })


@router.post("/product/{product_id}/order", name="submit_order")
async def submit_order(
        product_id: int,
        customer_name: str = Form(...),
        phone_number: str = Form(...),
        preferred_contact: str = Form(...),
        db: Session = Depends(get_db)
):
    product = db.query(models.Template).filter(models.Template.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Պրոդուկտը չի գտնվել")

    order_data = schemas.OrderCreate(
        customer_name=customer_name,
        phone_number=phone_number,
        preferred_contact=preferred_contact,
        template_id=product_id
    )

    order_service = OrderService(OrderRepository(db))
    order_service.create_order(order_data)

    return RedirectResponse(url=f"/product/{product_id}?order_success=true", status_code=303)