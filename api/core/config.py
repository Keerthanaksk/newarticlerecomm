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

    # jwt
    authjwt_secret_key: str = SECRET_KEY
    # Configure application to store and get JWT from cookies
    AUTHJWT_TOKEN_LOCATION: set = {"cookies"}
    # Disable CSRF Protection for this example. default is True
    AUTHJWT_COOKIE_CSRF_PROTECT: bool = False

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 60 # 1 hour
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 1 week


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