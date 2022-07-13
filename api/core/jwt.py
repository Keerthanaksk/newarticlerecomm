from api import crud
from api.schemas import ShowUser
from api.db.mongodb import get_database

from fastapi import Depends, HTTPException

from fastapi_jwt_auth import AuthJWT
# from fastapi_jwt_auth.exceptions import MissingTokenError

from motor.motor_asyncio import AsyncIOMotorDatabase

async def current_user(
    db: AsyncIOMotorDatabase = Depends(get_database),
    Authorize: AuthJWT = Depends()
) -> ShowUser:
    try:
        Authorize.jwt_required()
    except Exception as e:
        
        status_code = e.status_code
        
        raise HTTPException(status_code=status_code, detail="User not logged in")
    
    user = await crud.user.get_by_id(db, id=Authorize.get_jwt_subject())

    if not user:
        raise HTTPException(status_code=status_code, detail="User not found")
    
    return user