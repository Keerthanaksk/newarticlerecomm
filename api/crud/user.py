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

    async def get_interactions(self, db: AsyncIOMotorDatabase, length: int):
        '''
        Returns the article interactions per user

        Returns a list of dict:
            email: str
            links: List
                link: str
                loved: bool
                clicks: int
        '''

        users_collection = db[self.collection]

        try:
            result = users_collection.aggregate(
                [
                    {
                        '$lookup':
                        {
                            'from': crud.article.articleInteractions,
                            'localField': '_id',
                            'foreignField': 'user_id',
                            'as': 'links'
                        }
                    },
                    {
                        '$lookup':
                        {
                            'from': crud.article.collection,
                            'localField': 'links.link',
                            'foreignField': 'link',
                            'as': 'date'
                        }
                    },
                    {
                        '$addFields': 
                        {
                            'links.date': '$date.date_recommended'
                        }
                    }
                    # {
                    #     '$project': 
                    #     {
                    #         'password': 0,
                    #         'links._id': 0
                    #     }
                    # }
                ]
            )

            result = await result.to_list(length)

            from pprint import pprint

            pprint(result)


            return []
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500, 
                detail="An error occured while getting user interactions."
            )

        # lookup
        # id = user_id

        # exclude i





    # async def get_user_articles_stats(self, db: AsyncIOMotorDatabase):
    #     '''
    #         [
    #             {
    #                 id: objid
    #                 email: str,
    #                 articles : [
    #                     {
    #                         id: objid
    #                         link: str
    #                         loved: bool
    #                         clicks: int
    #                     },
    #                     ...
    #                 ]
    #             },
    #             ...
    #         ]

    #         users lookup loved 
    #         lookup clicked

    #         users
    #         -email
    #         -password

    #         articles
    #         -link
    #         -topic
    #         -summary
    #         -title

    #         articleInteractions
    #         -user_id
    #         -link
    #         -loved
    #         -clicks

    #         ====
    #         -how many articles would the user see per day?
    #         -ask if its a good idea to trust that the links will be unique since im indexing by link


    #         get articles
    #             - total_loves
    #                 - lookup articleinteractions
    #                 - count size where loved is true
    #             - loved (optional)
    #                 - cond in current_user, in users
    #             - total_clicks 
    #                 - sum clicks



            



        # '''



user = CRUDUser('users')