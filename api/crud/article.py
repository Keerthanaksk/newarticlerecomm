from typing import Union
from bson import ObjectId

from fastapi import HTTPException

from api.crud import CRUDBase

from motor.motor_asyncio import AsyncIOMotorDatabase

class CRUDArticle(CRUDBase):

    async def get_by_link(self, db: AsyncIOMotorDatabase, link: str, user_id: Union[str, None] = None):
        '''
            Working but not desired output

            Returns a list of single item containing the article
        '''
        user_id = ObjectId(user_id)
        collection = db[self.collection]

        try:
            article = await collection.find_one(
                {
                    '_id': user_id, 
                    'recommendations.link': link
                },
                {
                    'recommendations.$': 1
                }
            )
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500, 
                detail="An error occured while finding the article."
            )
            
        if not article:
            raise HTTPException(
                    status_code=404, 
                    detail="Article not found."
                )
        
        result = article['recommendations'][0]

        return result



    async def get_multi(self, db: AsyncIOMotorDatabase, length, filter=None, user_id=None):
        '''
        Get all articles recommended

        Returns a list of dictionary containing:
            id: ObjectId,
            link: str
            title: str
            topic: str
            summary: str
            total_loves: int
            total_clicks: int
        '''

        try:
            recommendations = db[self.collection].aggregate([
                {
                    '$unwind': '$recommendations'
                },
                {
                    '$replaceRoot': 
                    {
                        'newRoot': '$recommendations'
                    }
                },
                {
                    '$group': 
                    {
                        '_id': 
                        {
                            'link': '$link',
                            'topic': '$topic',
                            'title': '$title',
                            'summary': '$summary' 
                        },
                        'total_loves': 
                        {
                            '$sum': 
                            {
                                '$cond': ['$loved', 1, 0]
                            }
                        },
                        'total_clicks': {'$sum': '$clicks'}
                    }
                },
                {
                    '$project':
                    {
                        '_id': 0,
                        'link': '$_id.link',
                        'topic': '$_id.topic',
                        'title': '$_id.title',
                        'summary': '$_id.summary',
                        'total_loves': 1,
                        'total_clicks': 1,
                    }
                }
            ])

            recommendations = await recommendations.to_list(length)

            return recommendations
        
        except:
            raise HTTPException(
                status_code=404, 
                detail="An error occured while fetching articles."
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
        
        # get article to obtain 'loved' status
        article = await self.get_by_link(db, link, user_id=str(user_id))

        collection = db[self.collection]

        # update love
        try:
            result = await collection.update_one(
                    {
                        '_id': user_id, 
                        'recommendations.link': link
                    },
                    {'$set': {'recommendations.$.loved': not article['loved']}}
                )
        except:
            raise HTTPException(
                status_code=500, 
                detail="An error occured while updating loves."
            )

        if not result.modified_count:
            raise HTTPException(
                status_code=404, 
                detail="No article found for updating 'loved'."
            )
        
        return True



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
        collection = db[self.collection]

        # increment clicks
        try:
            result = await collection.update_one(
                    {
                        '_id': user_id, 
                        'recommendations.link': link
                    },
                    {'$inc': {'recommendations.$.clicks': 1}}
                )
        except:
            raise HTTPException(
                status_code=500, 
                detail="An error occured while updating clicks."
            )

        if not result.modified_count:
            raise HTTPException(
                status_code=404, 
                detail="No article found for updating 'clicks'."
            )
        
        return True



    async def get_topics(
        self,
        db: AsyncIOMotorDatabase,
        length: int,
        user_id: str
    ):
        '''
            Get topics of articles recommended for the user
        '''
        user_id = ObjectId(user_id)

        try:
            topics = db[self.collection].aggregate([
                {
                    '$match':
                    {
                        '_id': user_id
                    }
                },
                {
                    '$unwind': '$recommendations'
                },
                {
                    '$replaceRoot': 
                    {
                        'newRoot': '$recommendations'
                    }
                },
                {
                    '$group': 
                    {
                        '_id': '$topic'
                    }
                }
            ])

            topics = await topics.to_list(length)
            
            topics_list = {'topics': []}

            for t in topics:
                topics_list['topics'].append(t['_id'])

            return topics_list
        
        except Exception as e:
            raise HTTPException(
                status_code=404, 
                detail="An error occured while fetching topics."
            )
        

      

article = CRUDArticle('users')
