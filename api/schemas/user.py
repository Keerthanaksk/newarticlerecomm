from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field, validator, root_validator

from api.schemas.base_class import PKModel

class UserBase(BaseModel):
    username: Optional[str]

class ShowUser(UserBase, PKModel):
    username: str

class UserCreate(UserBase):
    username: str
    password: str

class UserInDB(UserBase, PKModel):
    username: str
    password: str