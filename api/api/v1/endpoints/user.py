from pprint import pprint
from typing import List, Optional
import os
import pandas as pd

from api import crud
from api.core import jwt, config
from api.schemas import ShowUser, UserCreate
from api.db.mongodb import get_database

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import io

from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()


@router.get('/', response_model=List[ShowUser])
async def get_users(
    limit: int = 100,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    users = await crud.user.get_multi(db, length=limit)
    return users

@router.get('/export')
async def export_users(
    limit: int = 100,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    recos = db.recommendationHistory.aggregate(
        [
            {
                '$unwind': '$recommendations'
            },
            {
                '$project':
                {
                    '_id': 1,
                    'email': 1,
                    'link': '$recommendations.link',
                    'clicks': '$recommendations.clicks',
                    'loved': '$recommendations.loved',
                    'date_recommended': '$recommendations.date_recommended'
                }
            }
        ]
    )
    recos = await recos.to_list(limit)
    
    df = pd.DataFrame.from_records(recos)
    
    stream = io.StringIO()

    df.to_csv(stream)

    response = StreamingResponse(iter([stream.getvalue()]),
                        media_type="text/csv"
    )

    response.headers["Content-Disposition"] = "attachment; filename=export.csv"

    return response

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
