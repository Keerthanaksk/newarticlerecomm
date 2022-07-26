from pprint import pprint
from typing import List, Union
from bson import ObjectId

from api.db.mongodb import get_database
from api.schemas import ShowArticle, ShowUser, ShowRecommendation
from api import crud
from api.core import jwt

from fastapi import APIRouter, Depends

from fastapi_jwt_auth import AuthJWT
from api.schemas.article import ShowTopics

from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

@router.get("/all", response_model=List[ShowArticle])
async def get_articles(
    limit: int = 100,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    '''
        Return all articles and total interactions

        Will not require loggin in anymore
    '''
    
    articles = await crud.article.get_multi(db, length=limit)
    
    return articles

@router.get("/recommendations", response_model=List[ShowRecommendation])
async def get_recommendations(
    topic: Union[str, None] = None,
    limit: int = 100,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: ShowUser = Depends(jwt.current_user)
):
    '''
        Return recommendations for the user

        Difference with /all is that this will also return
        loved -> Boolean
        total_clicks -> Int
    '''

    recommendations = await crud.article.get_recommendations(
        db, 
        length=limit, 
        topic=topic, 
        user_id=current_user['_id']
    )
    
    return recommendations


@router.post("/love")
async def love_by_link(
    link: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: ShowUser = Depends(jwt.current_user)
):
    '''
        Love/Unlove an article depending on the existing interaction
    '''
    
    
    article = await crud.article.love_by_link(
        db, 
        link=link,
        user_id=current_user['_id']
    )
    
    
    return article



@router.post("/click")
async def click_by_link(
    link: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: ShowUser = Depends(jwt.current_user) 
):
    '''
        Increase article's click interactions
    '''

    clicked = await crud.article.click_by_link(
        db, 
        link=link,
        user_id=current_user['_id']
    )
    
    return clicked



@router.get('/topics', response_model=ShowTopics)
async def get_topics(
    limit: int = 100,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: ShowUser = Depends(jwt.current_user)
):
    '''
    Get topics of articles recommended for the user
    '''

    topics = await crud.article.get_topics(
        db,
        length=limit,
        user_id=current_user['_id']
    )

    return topics
