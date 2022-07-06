from copyreg import constructor
from typing import Optional, List, Union

from api.crud import article
from api.db.mongodb import get_database
from api.schemas import ShowArticle, ShowUser
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
    db: AsyncIOMotorDatabase = Depends(get_database),
    Authorize: AuthJWT = Depends()
):
    '''
        Return articles with love counts

        Optionally, it can return 'loved' as True of False if an article is loved by the current user
    '''
    Authorize.jwt_optional()
    
    user_id = Authorize.get_jwt_subject()
    
    filter = {}
    
    if topic:
        filter['topic'] = topic
    
    articles = await crud.article.get_multi(db, limit, filter, loved_by_user_id=user_id)
    
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


# @app.get("/{id}")
# async def get_by_id(id):
#     oid = ObjectId(id)
#     article = await coll.find_one({'_id': oid})
    
#     article = {
#         'id': str(article['_id']), 
#         'link': article['link'],
#         'topic': article['topic'],
#         'summary': article['summary'],
#         'clicked': article['clicked'],
#         'liked': article['liked'],
#         'clicks': article['clicks'],
#         'loves': article['loves']
#     }
#     return article
