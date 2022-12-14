import os

from api.core.config import settings
from api.db.mongodb_utils import connect_to_mongo, close_mongo_connection
from api.db.recommendations import get_recommendations
from api.api.v1.api import api_router

from starlette.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from fastapi_jwt_auth import AuthJWT


def register_cors(app: FastAPI):
    
    if os.environ.get('FASTAPI_ENV') == 'prod':
        origins = [
            os.environ.get('FRONTEND_ORIGIN')
        ]
    else:
        origins = [
            'http://localhost:8080'
        ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins, # resource exchange
        allow_credentials=True, # cookies and sensitive info
        allow_methods=["*"], # POST, GET, etc.
        allow_headers=["*"], # additional information in requests
    )


def register_fastapi_jwt_auth(app: FastAPI):
    @AuthJWT.load_config
    def get_config():
        return settings

def register_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        get_recommendations, 
        'interval',
        minutes=5
        # seconds=10
        # 'cron', 
        # hour=21, 
        # minute=0, 
        # timezone='Asia/Manila'
    )
    scheduler.start()

def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME, 
        description=settings.PROJECT_DESC,
        version=settings.PROJECT_VERSION
    )

    app.include_router(api_router)

    app.add_event_handler("startup", connect_to_mongo)
    # app.add_event_handler("startup", register_scheduler)
    app.add_event_handler("shutdown", close_mongo_connection)

    register_cors(app)
    register_fastapi_jwt_auth(app)

    return app

