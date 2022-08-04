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

    # secure signing
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'secret')
    
    # mongodb source
    MONGO_URL: str = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')
    
    # database to use
    MONGO_DB: str = os.environ.get('MONGO_DB', 'unionbank')

    # secret key
    authjwt_secret_key: str = SECRET_KEY
    
    # Configure application to store and get JWT from cookies
    # httponly cookies
    AUTHJWT_TOKEN_LOCATION: set = {"cookies"}
    
    # Disable CSRF Protection for this example. default is True
    AUTHJWT_COOKIE_CSRF_PROTECT: bool = False

    # expiry
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 60 # 1 hour
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 1 week

class DevelopmentSettings(Settings):
    # can be sent through HTTP
    authjwt_cookie_secure: bool = False



class ProductionSettings(Settings):
    # CORS
    authjwt_cookie_samesite: str = 'none'
    
    # HTTPS ONLY
    authjwt_cookie_secure: bool = True



def load_settings():
    if os.environ.get('FASTAPI_ENV') == 'prod':
        return ProductionSettings()
    else:
        return DevelopmentSettings()



settings = load_settings()