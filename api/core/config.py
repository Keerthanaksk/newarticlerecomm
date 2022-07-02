import os, secrets
from dotenv import load_dotenv
from pydantic import BaseSettings

env_path = '.env'
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    PROJECT_NAME: str = "Intelligent Newsletter"
    PROJECT_DESC: str = """UnionBank articles recommender prototype"""
    PROJECT_VERSION: str = "1.0.0"

    SECRET_KEY: str = secrets.token_urlsafe(32) 
    MONGO_URL: str
    MONGO_DB: str


class DevelopmentSettings(Settings):
    pass



class ProductionSettings(Settings):
    pass



def load_settings():
    if os.getenv('FASTAPI_ENV') == 'prod':
        return ProductionSettings()
    else:
        return DevelopmentSettings()



settings = load_settings()