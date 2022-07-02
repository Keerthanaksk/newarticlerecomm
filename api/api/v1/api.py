from fastapi import APIRouter
from api.api.v1.endpoints import user

api_router = APIRouter()
api_router.include_router(user.router, prefix='/user', tags=['user'])
# api_router.include_router(article.router, prefix='/article', tags=['article'])