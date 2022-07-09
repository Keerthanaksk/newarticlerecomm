from copyreg import constructor
from typing import Optional, List, Union

from api.crud import article
from api.db.mongodb import get_database
from api.schemas import ShowArticle, ShowUser, ArticleStats
from api import crud
from api.core import jwt

from fastapi import APIRouter, Depends, HTTPException

from fastapi_jwt_auth import AuthJWT

from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

@router.get("/", response_model=List[ShowArticle])
async def get_articles(
    topic: Union[str, None] = None,
    limit: int = 100,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    '''
        Return articles with love and click counts
    '''
    
    filter = {}
    
    if topic:
        filter['topic'] = topic
    
    articles = await crud.article.get_multi(db, limit, filter)
    
    return articles



@router.post("/love/{id}", response_model=ShowArticle)
async def love_article_by_id(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: ShowUser = Depends(jwt.current_user) 
):
    '''
        Returns the article with loves count
    '''
    article = await crud.article.love_article_by_id(db, id=id, user_id=current_user['_id'])
    
    return article



@router.post("/unlove/{id}", response_model=ShowArticle)
async def unlove_article_by_id(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: ShowUser = Depends(jwt.current_user) 
):
    '''
        Removes love and returns the article with loves count
    '''
    print('unlove',current_user['_id'])
    article = await crud.article.unlove_article_by_id(db, id=id, user_id=current_user['_id'])
    
    return article



@router.post("/click/{id}")
async def click_article_by_id(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: ShowUser = Depends(jwt.current_user) 
):
    '''
        Mark the article as clicked by the user

        Clicks can duplicate but not loves
    '''

    clicked = await crud.article.click_article_by_id(db, id=id, user_id=current_user['_id'])
    
    if not clicked:
        raise HTTPException(status_code=500, detail="Article click was not registered")
    
    return {'detail': 'Successfully clicked'}



@router.post("/articles-stats", response_model=List[ArticleStats])
async def articles_stats(
    limit: int = 100,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: ShowUser = Depends(jwt.current_user)
):
    '''
        See stats of articles read(clicked Read more) and loved by the user
    '''

    articles = await crud.article.articles_stats(db, limit, user_id=current_user['_id'])

    return articles

