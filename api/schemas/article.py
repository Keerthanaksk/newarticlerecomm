from typing import Optional
from api.schemas.base_class import PKModel

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
    loves: int
    loved: Optional[bool]
    

class ArticleCreate(ArticleBase):
    pass