from typing import List, Optional
import os

from api import crud
from api.core import jwt
from api.schemas import ShowUser, UserCreate
from api.db.mongodb import get_database

from fastapi import APIRouter, Depends

from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

@router.get('/')
async def test():
    return {'msg': os.environ.get('FRONTEND_ORIGIN')}

@router.get('/', response_model=List[ShowUser])
async def get_users(
    limit: int = 100,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    users = await crud.user.get_multi(db, length=limit)
    return users

@router.get('/test')
async def test():
    x = os.environ.get('TEST')
    return {'x':x}


@router.get('/id/{id}', response_model=ShowUser)
async def get_user_by_id(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    user = await crud.user.get_by_id(db, id)
    return user

@router.post('/', response_model=ShowUser)
async def create_user(
    user_in: UserCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # catch duplicates
    result = await crud.user.create(db, user_in)
    created_user = await crud.user.get_by_id(db, str(result.inserted_id))
    
    return created_user

@router.get('/current-user', response_model=ShowUser)
async def get_current_user(
    current_user: ShowUser = Depends(jwt.current_user)
):
    return current_user