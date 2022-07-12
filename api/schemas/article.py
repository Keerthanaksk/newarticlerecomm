from typing import Optional, List
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime

from api.schemas.base_class import PKModel

class ArticleBase(BaseModel):
    link: Optional[str]
    title: Optional[str]
    topic: Optional[str]
    summary: Optional[str]
    total_loves: Optional[int]
    total_clicks: Optional[int]

class ShowArticle(ArticleBase):
    pass

class ShowArticleInteraction(BaseModel):
    # article_id: str
    link: str
    loved: bool
    clicks: int
    date_recommended: datetime

class ShowTopics(BaseModel):
    topics: List[str]