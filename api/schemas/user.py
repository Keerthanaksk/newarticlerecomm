from bson import ObjectId
from typing import List, Optional, Union
from pydantic import BaseModel, Field, validator, root_validator

from api.schemas import ShowArticleInteraction

from api.schemas.base_class import PKModel

class UserBase(BaseModel):
    email: Optional[str]

class ShowUser(UserBase):
    email: str
    recommendations: List[ShowArticleInteraction]

class UserCreate(UserBase):
    email: str
    password: str

class UserInDB(UserBase, PKModel):
    email: str
    password: str