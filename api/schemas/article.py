from typing import Optional

import click
from pydantic import BaseModel
from api.schemas.base_class import PKModel
from bson import ObjectId

class ArticleBase:
    link: Optional[str]
    title: Optional[str]
    topic: Optional[str]
    summary: Optional[str]
    loves: Optional[int]
    loved: Optional[bool]

class ShowArticle(ArticleBase, PKModel):
    link: str
    title: str
    topic: str
    summary: str
    total_loves: int
    total_clicks: int

class ArticleCreate(ArticleBase):
    pass

class ArticleStats(ArticleBase, PKModel):
    link: str
    title: str
    topic: str
    summary: str
    loves: int
    loved: Optional[bool]
    clicks: int

class CreateArticleInteraction(BaseModel):
    link: str
    user_id: ObjectId
    loved: bool
    clicks: int = 0

    class Config:
        arbitrary_types_allowed = True
