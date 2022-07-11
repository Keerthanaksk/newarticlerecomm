from copyreg import constructor
from typing import Optional, List, Union

from api.crud import article
from api.db.mongodb import get_database
from api.schemas import ShowArticle, ShowUser
from api import crud
from api.core import jwt

from fastapi import APIRouter, Depends

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
        Return articles 
    '''

    Authorize.jwt_optional()

    user_id = Authorize.get_jwt_subject()

    filter = {}
    
    if topic:
        filter['topic'] = topic
    
    articles = await crud.article.get_multi(db, length=limit, filter=filter, user_id=user_id)
    
    return articles



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

