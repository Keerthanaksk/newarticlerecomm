from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

# path is dependent on the level where you executed uvicorn server startup command
templates = Jinja2Templates(directory="api/templates")

@router.get('/')
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
