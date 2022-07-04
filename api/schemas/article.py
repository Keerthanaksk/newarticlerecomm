from typing import Optional
from api.schemas.base_class import PKModel

class ArticleBase:
    link: Optional[str]
    topic: Optional[str]
    summary: Optional[str]
    loves: Optional[int]

class ShowArticle(ArticleBase, PKModel):
    link: str
    topic: str
    summary: str
    loves: int

class ArticleCreate(ArticleBase):
    pass