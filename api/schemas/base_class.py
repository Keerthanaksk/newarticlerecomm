from pydantic import BaseModel, root_validator

class PKModel(BaseModel):
    '''
        Base model class that adds the ObjectId column named 'id'
    '''

    id: str

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
