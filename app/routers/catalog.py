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
    return html_templates.TemplateResponse("catalog_new.html", {
        "request": request,
        "templates": all_products
    })