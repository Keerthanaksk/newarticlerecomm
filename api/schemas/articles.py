from pydantic import BaseModel

class ArticleBase(BaseModel):
    title: str
    topic: str
    link: str
    summary: str

class ShowArticle(ArticleBase):
    clicked: bool
    liked: bool
    clicks: int
    loves: int