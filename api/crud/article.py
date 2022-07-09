from tokenize import group
from typing import Union
from bson import ObjectId
import pandas as pd
import logging

from fastapi import HTTPException

from api.crud import CRUDBase
from api.schemas import CreateArticleInteraction

from motor.motor_asyncio import AsyncIOMotorDatabase

class CRUDArticle(CRUDBase):
    
    # association collections
    # loved_articles = 'lovedArticles'
    # clicked_articles = 'clickedArticles'
    articleInteractions = 'articleInteractions'

    async def get_by_link(self, db, link: str, user_id: Union[str, None] = None):
        collection = db[self.collection]

        article = await collection.find_one({'link': link})
        # loves = await self.count_loves(db, link)
        
        if not article:
            raise HTTPException(
                    status_code=404, 
                    detail="Article not found."
                )
        
        result = {**article}
        
        if user_id:
            result['loved'] = await self.is_loved_by_user(db, id, user_id=user_id)

        return result



    async def get_multi(self, db: AsyncIOMotorDatabase, length, filter=None, user_id=None):
        '''
        Returns:
            A list of dictionary containing:
                id: ObjectId,
                link: str
                title: str
                topic: str
                summary: str
                total_loves: int
                total_clicks: int
                loved: Optional(bool)

        '''
        
        # fields to show
        project = {
            '$project': 
            {
                'link': 1,
                'title': 1,
                'topic': 1,
                'summary': 1,
                'total_loves': 
                {
                    '$size': 
                    {
                        '$filter':
                        {
                            'input': '$user_interactions',
                            'as': 'interactions',
                            'cond': { '$eq': ['$$interactions.loved', True]}
                        }

                    }
                },
                'total_clicks': {'$sum': '$user_interactions.clicks'}
            }
        }

        # adds a field to indicate if article is loved by the given user
        if user_id:
            user_id = ObjectId(user_id)
            
            project['$project']['loved'] = {
                '$cond': 
                [
                    {'$in': [user_id, '$user_interactions.user_id']}, True, False
                ]
            }

        try:
            result = db[self.collection].aggregate(
                [
                    # filter 
                    {
                        '$match': filter if filter else {}
                    },
                    
                    # Joining with articleInteractions collection
                    {
                        '$lookup': 
                        {
                            'from': self.articleInteractions,
                            'localField': 'link',
                            'foreignField': 'link',
                            'as': 'user_interactions'
                        },
                    },

                    # fields to show
                    project
                ]
            )
            
            result = await result.to_list(length)

            return result

        except Exception as e:
            logging.error(e)
            
            raise HTTPException(
                status_code=500, 
                detail="An error occured while getting articles."
            )
        



    async def love_by_link(
        self, 
        db: AsyncIOMotorDatabase, 
        user_id: str, 
        link: str
    ):
        '''
            Love/Unlove an article depending on the existing interaction
        '''
        
        user_id = ObjectId(user_id)
        collection = db[self.articleInteractions]

        # check if article exists
        article = await self.get_by_link(db, link)

        # get the interaction
        query = {'user_id': user_id, 'link': link}
        article_interaction = await collection.find_one(
            query
        )
        
        # setting function
        set_loved = lambda b : collection.update_one(
            query,
            {'$set': {'loved': b}}
        )
        
        try:
            if article_interaction:
                # if interaction exists and loved -> False
                if article_interaction.get('loved'):
                    await set_loved(False)

                # else if it exists and not loved -> True
                else:
                    await set_loved(True)

            else:
                # if it doesnt exist, create the loved interaction
                await collection.insert_one(
                    CreateArticleInteraction(
                        link=link,
                        user_id=user_id,
                        loved=True,
                        clicks=0
                    ).dict()
                )

            return True
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500, 
                detail="An error occured while updating the love interaction."
            )



    # async def count_loves(self, db: AsyncIOMotorDatabase, id: str):
    #     id = ObjectId(id)

    #     loves = await db[self.loved_articles].count_documents({'article_id': id})
        
    #     return loves



    # async def is_loved_by_user(self, db: AsyncIOMotorDatabase, id: str, user_id=None):
    #     id = ObjectId(id)
    #     user_id = ObjectId(user_id)

    #     loved = await db[self.loved_articles].find_one({'article_id': id, 'user_id': user_id})
        
    #     if not loved:
    #         return False

    #     return True



    async def click_by_link(
        self, 
        db: AsyncIOMotorDatabase, 
        link: str, 
        user_id: str
    ):
        '''
            Increment/Create the click interaction of an article
        '''
        user_id = ObjectId(user_id)
        collection = db[self.articleInteractions]

        # check if article exists
        article = await self.get_by_link(db, link)

        # get the interaction
        query = {'user_id': user_id, 'link': link}
        article_interaction = await collection.find_one(
            query
        )

        try:
            if article_interaction:
                # if interaction exists, inc clicks
                await collection.update_one(
                    query,
                    {'$inc': {'clicks': 1}}
                )
                
            else:
                # if it doesnt exist, create the interaction
                await collection.insert_one(
                    CreateArticleInteraction(
                        link=link,
                        user_id=user_id,
                        loved=False,
                        clicks=1
                    ).dict()
                )

            return True
        except:
            raise HTTPException(
                status_code=500, 
                detail="An error occured while updating the click interaction."
            )



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