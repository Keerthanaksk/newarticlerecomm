from bson import ObjectId

from api.crud import CRUDBase

from motor.motor_asyncio import AsyncIOMotorDatabase

class CRUDArticle(CRUDBase):
    
    # association collections
    loved_articles = 'lovedArticles'
    clicked_articles = 'clickedArticles'

    async def get_by_id(self, db, id: str):
        article = await super().get_by_id(db, id)
        loves = await self.count_loves(db, id)
        return {**article, 'loves': loves}

    async def get_multi(self, db: AsyncIOMotorDatabase, length, filter=None):
        
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
                
                # Columns to show
                {
                    '$project': {
                        'link': 1,
                        'title': 1,
                        'topic': 1,
                        'summary': 1,
                        'loves': {'$size': '$users'}
                    }
                }
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
        
        article = await self.get_by_id(db, id)
        
        return {**article}

    async def unlove_article_by_id(self, db: AsyncIOMotorDatabase, id: str, user_id: str):
        id = ObjectId(id)
        user_id = ObjectId(user_id)

        result = await db[self.loved_articles].delete_one({'user_id': user_id, 'article_id': id})
        
        article = await self.get_by_id(db, id)
        
        return {**article}

    async def count_loves(self, db: AsyncIOMotorDatabase, id: str):
        id = ObjectId(id)

        loves = await db[self.loved_articles].count_documents({'article_id': id})

        return loves

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