from motor.motor_asyncio import AsyncIOMotorDatabase
from api.schemas import UserCreate
from api.crud import CRUDBase

class CRUDUser(CRUDBase):

    async def get_by_id(self, db: AsyncIOMotorDatabase, id: str):
        return await super().get_by_id(db, id=id)

    async def get_multi(self, db: AsyncIOMotorDatabase, length):
        return await super().get_multi(db, length)

    async def create(self, db: AsyncIOMotorDatabase, obj_in: UserCreate):
        # bcrypt pw
        return await super().create(db, obj_in=obj_in)

user = CRUDUser('user')