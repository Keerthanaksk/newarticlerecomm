import os

from api.core.config import settings
from api.db.mongodb_utils import connect_to_mongo, close_mongo_connection
from api.api.v1.api import api_router

from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI



def register_cors(app: FastAPI):
    
    if os.getenv('FASTAPI_ENV') == 'prod':
        origins = [
            os.getenv('FRONTEND_ORIGIN')
        ]
    else:
        origins = [
            'http://localhost:8080'
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME, 
        description=settings.PROJECT_DESC,
        version=settings.PROJECT_VERSION
    )

    app.include_router(api_router)

    app.add_event_handler("startup", connect_to_mongo)
    app.add_event_handler("shutdown", close_mongo_connection)

    register_cors(app)

    return app

