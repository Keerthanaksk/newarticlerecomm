from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field, validator, root_validator

class UserBase(BaseModel):
    username: Optional[str]

class ShowUser(UserBase):
    id: str
    username: str

    @root_validator(pre=True)
    def cast_objectid_to_string(cls, values):
        '''
            Cast raw ObjectId types to string before field validation
        '''
        if values.get('_id'):
            values['_id'] = str(values['_id'])
        if values.get('id'):
            values['id'] = str(values['id'])

        return values

    class Config:
        fields = {'id': '_id'}


class UserCreate(UserBase):
    username: str
    password: str