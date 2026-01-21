from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
html_templates = Jinja2Templates(directory="templates")


@router.get("/", name="home")
def home(request: Request):
    return html_templates.TemplateResponse("home.html", {"request": request})