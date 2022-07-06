from typing import Union
from bson import ObjectId

from api.crud import CRUDBase

from motor.motor_asyncio import AsyncIOMotorDatabase

class CRUDArticle(CRUDBase):
    
    # association collections
    loved_articles = 'lovedArticles'
    clicked_articles = 'clickedArticles'

    async def get_by_id(self, db, id: str, user_id: Union[str, None] = None):
        article = await super().get_by_id(db, id)
        loves = await self.count_loves(db, id)
        
        result = {**article, 'loves': loves}
        
        if user_id:
            result['loved'] = await self.is_loved_by_user(db, id, user_id=user_id)
        
        return result



    async def get_multi(self, db: AsyncIOMotorDatabase, length, filter=None, loved_by_user_id=None):
        
        # fields to show
        project = {
            '$project': {
                'link': 1,
                'title': 1,
                'topic': 1,
                'summary': 1,
                'loves': {'$size': '$users'}
            }
        }

        # adds a field to indicate if article is loved by the given user
        if loved_by_user_id:
            loved_by_user_id = ObjectId(loved_by_user_id)
            project['$project']['loved'] = {'$cond': [ {'$in': [ loved_by_user_id, '$users.user_id']}, True, False]}

        result = db[self.collection].aggregate(
            [
                # filter 
                {
                    '$match': filter if filter else {}
                },
                
                # Joining collections
                {
                    '$lookup': 
                    {
                        'from': 'lovedArticles',
                        'localField': '_id',
                        'foreignField': 'article_id',
                        'as': 'users'
                    },
                },
                project
            ]
        )
        
        result = await result.to_list(length)
        
        return result



    async def love_article_by_id(self, db: AsyncIOMotorDatabase, id: str, user_id: str):
        id = ObjectId(id)
        user_id = ObjectId(user_id)

        collection = db[self.loved_articles]
        operation = {'user_id': user_id, 'article_id': id}
        
        # check if article is already loved by the user
        article = await collection.find_one(
            operation
        )

        if not article:
            # create association
            article = await collection.insert_one(operation)
        
        article = await self.get_by_id(db, id, str(user_id))
        
        return {**article}



    async def unlove_article_by_id(self, db: AsyncIOMotorDatabase, id: str, user_id: str):
        id = ObjectId(id)
        user_id = ObjectId(user_id)

        result = await db[self.loved_articles].delete_one({'user_id': user_id, 'article_id': id})
        
        article = await self.get_by_id(db, id, str(user_id))
        
        return {**article}



    async def count_loves(self, db: AsyncIOMotorDatabase, id: str):
        id = ObjectId(id)

        loves = await db[self.loved_articles].count_documents({'article_id': id})
        
        return loves



    async def is_loved_by_user(self, db: AsyncIOMotorDatabase, id: str, user_id=None):
        id = ObjectId(id)
        user_id = ObjectId(user_id)

        loved = await db[self.loved_articles].find_one({'article_id': id, 'user_id': user_id})
        
        if not loved:
            return False

        return True



    async def click_article_by_id(self, db: AsyncIOMotorDatabase, id: str, user_id: str):
        id = ObjectId(id)
        user_id = ObjectId(user_id)

        collection = db[self.clicked_articles]
        operation = {'user_id': user_id, 'article_id': id}
        
        article = await collection.insert_one(
            operation
        )
        
        article = await collection.find_one(
            operation
        )

        if not article:
            False
        
        return True



article = CRUDArticle('articles')

# def get_articles():
#     articles = fetch

# # not sure kung str ang id
# def get_article_by_id(id: str):
#     article = 

#     return article

# def update_article_loves_by_id(id: str):
#     article

#     if fail:
#         return 0
    
#     return 1

# def update_article_clicked_by_id

# def update_article_clicks_by_id