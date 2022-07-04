from api.core.security import get_password_hash
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

class CRUDBase:

    def __init__(self, collection: str) -> None:
        self.collection = collection
        
    async def get_by_id(self, db, id: str):
        '''
            Get user by ObjectId 

            id -> string form of ObjectId

            Returns with the ObjectId casted to string
        '''
        
        id = ObjectId(id)
        result = await db[self.collection].find_one({'_id': id})
        result['_id'] = str(result['_id'])

        return result

    async def get_multi(self, db, length, filter = None):
        result = db[self.collection].find(filter if filter else {}) # find doesnt use await
        result = await result.to_list(length)
        return result

    async def create(self, db, obj_in):
        obj_in = jsonable_encoder(obj_in)
        obj_in['password'] = get_password_hash(obj_in['password']) # encrypt
        result = await db[self.collection].insert_one(obj_in)
        return result
    
    # async def update(self, db, id: ObjectId):
    #     result = await db[self.collection].({'_id': id})
        
    #     return result

    