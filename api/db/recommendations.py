import pandas as pd
import datetime as dt

from pprint import pprint
from typing import List
from api.db.mongodb import get_database
from api import crud
from api.schemas import ShowUser

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from pydantic import parse_obj_as

async def store_to_recommendation_history(db, limit, users):
    df = pd.DataFrame(users)
    
    # drop cols
    df.drop(["_id"], axis=1, inplace=True)
    df.drop(["password"], axis=1, inplace=True)
    
    # remove new users (those w/o recommended articles)
    df = df[df.recommendations.str.len() > 0]
    
    # convert to key-value pairs
    df = df.to_dict(orient='records')

    # insert to history collection
    result = await db.recommendationHistory.insert_many(df)
    
async def get_random_recommendations(db):
    recommendations = db.articles.aggregate([{ '$sample': { 'size': 15 } }])
    recommendations = await recommendations.to_list(15)
    
    df = pd.DataFrame(recommendations)

    # retain cols

    # loved col
    df['loved'] = False
    
    # clicks col
    df['clicks'] = 0

    # add date
    df['date_recommended'] = dt.datetime.now(dt.timezone.utc)

    # retain columns
    df = df[['link','date_recommended','loved','clicks']]

    df = df.to_dict(orient='records')

    return df

async def get_recommendations():
    limit = 100
    db = await get_database()
    
    # get users
    users = await crud.user.get_multi(db, length=limit)
    
    # store current recos to history
    await store_to_recommendation_history(db, limit, users)
    
    # fetch 15 random articles as new recommendations
    for user in users:
        # Recommend only to those w/ past recommendations (old users)
        if user['recommendations']:
            recos = await get_random_recommendations(db)
            result = await db.users.update_one(
                {'email': user['email']}, 
                {'$set': {'recommendations': recos}}
            )
    
    print('Recommended new articles!')
    
