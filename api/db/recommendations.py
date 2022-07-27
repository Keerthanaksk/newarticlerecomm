from pprint import pprint
from typing import List
from api.db.mongodb import get_database
from api import crud
from api.schemas import ShowUser

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from pydantic import parse_obj_as

async def test(y):
    # print(y)
    return y

async def get_recommendations():
    limit = 100
    db = await get_database()
    
    users = await crud.user.get_multi(db, length=limit)
    users = parse_obj_as(List[ShowUser], users).dict()
    pprint(users)
    # result = await db.recommendationHistory.insert_many()
    # store current recos to history
    # for u in users:
    #     pprint(u)
    # fetch 15 random
    # set as recommendations
    