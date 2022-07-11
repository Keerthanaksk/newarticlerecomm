from bson import ObjectId
from typing import List, Optional, Union
from pydantic import BaseModel, Field, validator, root_validator

from api.schemas import ShowArticleInteractions

from api.schemas.base_class import PKModel

class UserBase(BaseModel):
    email: Optional[str]

class ShowUser(UserBase, PKModel):
    email: str

class UserCreate(UserBase):
    email: str
    password: str

class UserInDB(UserBase, PKModel):
    email: str
    password: str

class ShowUserInteractions(UserBase):
    email: str
    links: Union[List[ShowArticleInteractions], None] = None
