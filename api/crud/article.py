from tokenize import group
from typing import Union
from bson import ObjectId
import pandas as pd

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



    async def get_multi(self, db: AsyncIOMotorDatabase, length, filter=None):
        '''
        [
            {
                id: objid,
                link: str
                title: str
                topic: str
                summary: str
                total_loves: int
                total_clicks: int
            },
            ...
        ]
        
        '''
        
        # fields to show
        project = {
            '$project': {
                'link': 1,
                'title': 1,
                'topic': 1,
                'summary': 1,
                'total_loves': {'$size': '$users_loved'},
                'total_clicks': {'$size': '$users_clicked'}
            }
        }

        # adds a field to indicate if article is loved by the given user
        # if loved_by_user_id:
        #     loved_by_user_id = ObjectId(loved_by_user_id)
        #     project['$project']['loved'] = {'$cond': [ {'$in': [ loved_by_user_id, '$users.user_id']}, True, False]}

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
                        'as': 'users_loved'
                    },
                },

                {
                    '$lookup': 
                    {
                        'from': 'clickedArticles',
                        'localField': '_id',
                        'foreignField': 'article_id',
                        'as': 'users_clicked'
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



    async def articles_stats(self, db: AsyncIOMotorDatabase, length, user_id: str):
        '''
            articles lookup lovedarticles count loves
            loved check if loved by user
            clicks by user for this article

            filter loved articles by user_id - get article ids
            filter clicks by user_id, group by article id, sum clicks
        '''
        
        user_id = ObjectId(user_id)

        # clickedarticles filter by user_id, 
        # group by articles and count clicks
        clicked = db[self.clicked_articles].find({'user_id': user_id})
        clicked = pd.DataFrame(await clicked.to_list(length))
        clicked = clicked.drop(columns=['_id', 'user_id'])
        clicked['clicks'] = 1
        clicked = pd.DataFrame(clicked.groupby(['article_id']).sum())
        clicked = clicked.reset_index()
        
        # lovedarticles filter by user_id, 
        loved = db[self.loved_articles].find({'user_id': user_id})
        loved = pd.DataFrame(await loved.to_list(length))
        loved = loved.drop(columns=['_id', 'user_id'])
        
        # combine articles in loved and clicked
        article_ids = []
        article_ids.extend(clicked['article_id'].tolist())
        article_ids.extend(loved['article_id'].tolist())

        article_ids = list(set(article_ids))

        # get articles loved or clicked by the user
        filter = {
            '_id': {'$in': article_ids}
        }
        
        articles = await self.get_multi(db, length, filter=filter, loved_by_user_id=str(user_id))
        articles = pd.DataFrame(articles)
        
        # rename clicked article_id col to _id
        clicked = clicked.rename(columns={'article_id':'_id'})

        # join clicked counts
        joined = articles.join(clicked.set_index('_id'), on='_id')

        # convert NaN to 0
        joined['clicks'] = joined['clicks'].fillna(0).astype('int')

        # objectid to string
        joined['_id'] = joined['_id'].astype('str')

        return joined.to_dict('records')
        


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