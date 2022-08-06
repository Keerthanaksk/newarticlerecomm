from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from api.core.config import settings

router = APIRouter()

# path is dependent on the level where you executed uvicorn server startup command
templates = Jinja2Templates(directory="api/templates")

@router.get('/')
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get('/test')
async def test(
	
):
	"""
	Print an env here
	"""

	return {'TEST_ENV': settings.TEST_ENV}