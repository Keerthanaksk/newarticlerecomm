from datetime import timedelta

from api import crud
from api.core.config import settings
from api.db.mongodb import get_database

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_jwt_auth import AuthJWT

from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

@router.post('/login')
async def login(
    db: AsyncIOMotorDatabase = Depends(get_database),
    user_in: OAuth2PasswordRequestForm = Depends(),
    Authorize: AuthJWT = Depends()
):
    user = await crud.user.authenticate(db, email=user_in.username, password=user_in.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = Authorize.create_access_token(
        subject=user.id, 
        fresh=True,
        expires_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
	
    refresh_token = Authorize.create_refresh_token(
        subject=user.id,
        expires_time=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)    
    )

    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)

    return user

@router.post('/logout')
async def logout(
	Authorize: AuthJWT = Depends(),
	# db: AsyncIOMotorDatabase = Depends(get_database)
):
	"""
	Revoke and unset access and refresh tokens
	"""

	# Authorize.jwt_required()
	# crud.token.revoke_access(Authorize, db)
	
	# Authorize.jwt_refresh_token_required()
	# crud.token.revoke_refresh(Authorize, db)

	Authorize.unset_jwt_cookies()

	return {'msg':'Successfully logged out.'}
