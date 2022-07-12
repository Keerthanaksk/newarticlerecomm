from api.core.security import verify_password
from api.schemas.user import UserInDB
from motor.motor_asyncio import AsyncIOMotorDatabase
from api.schemas import UserCreate
from api import crud
from api.crud import CRUDBase

from fastapi import HTTPException

class CRUDUser(CRUDBase):

    async def get_by_id(self, db: AsyncIOMotorDatabase, id: str):
        return await super().get_by_id(db, id=id)

    async def get_multi(self, db: AsyncIOMotorDatabase, length):
        return await super().get_multi(db, length=length)



    async def get_by_email(self, db: AsyncIOMotorDatabase, email: str):
        user = await db[self.collection].find_one({'email': email})
        if user:
            return UserInDB(**user)



    async def create(self, db: AsyncIOMotorDatabase, obj_in: UserCreate):
        # bcrypt pw
        return await super().create(db, obj_in=obj_in)



    async def authenticate(self, db: AsyncIOMotorDatabase, email: str, password: str):
        user = await self.get_by_email(db, email=email)

        if not user:
            return None
        
        if not verify_password(password, user.password):
            return None

        return user


user = CRUDUser('users')