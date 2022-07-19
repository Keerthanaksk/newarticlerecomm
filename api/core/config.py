import os, secrets
# from dotenv import load_dotenv
from pydantic import BaseSettings

# env_path = '.env'
# load_dotenv(dotenv_path=env_path)
# load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Intelligent Newsletter"
    PROJECT_DESC: str = """UnionBank articles recommender prototype"""
    PROJECT_VERSION: str = "1.0.0"

    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'secret')
    MONGO_URL: str = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')
    MONGO_DB: str = os.environ.get('MONGO_DB', 'unionbank')

    # jwt
    authjwt_secret_key: str = SECRET_KEY
    # Configure application to store and get JWT from cookies
    AUTHJWT_TOKEN_LOCATION: set = {"cookies"}
    # Disable CSRF Protection for this example. default is True
    AUTHJWT_COOKIE_CSRF_PROTECT: bool = False

    authjwt_cookie_samesite: str = 'none'

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 60 # 1 hour
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 1 week

class DevelopmentSettings(Settings):
    authjwt_cookie_secure: bool = False



class ProductionSettings(Settings):
    authjwt_cookie_secure: bool = True



def load_settings():
    if os.environ.get('FASTAPI_ENV') == 'prod':
        return ProductionSettings()
    else:
        return DevelopmentSettings()



settings = load_settings()