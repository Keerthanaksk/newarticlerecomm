from os import link
from pprint import pprint
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
            article = collection.aggregate([
                {
                    '$match':
                    {
                        '_id': user_id,
                        'recommendations.link': link
                    }
                },
                {
                    '$unwind': '$recommendations'
                },
                {
                    '$match':
                    {
                        'recommendations.link': link
                    }
                },
                {
                    '$project':
                    {
                        'recommendations': 1
                    }
                }
            ])
            article = await article.to_list(100)
            # article = await collection.find_one(
            #     {
            #         '_id': user_id, 
            #         'recommendations.link': link
            #     },
            #     {
            #         'recommendations.$': 1
            #     }
            # )
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
        
        result = article[0]['recommendations']

        return result



    async def get_multi(self, db: AsyncIOMotorDatabase, length):
        '''
        Get all articles
        
        Returns a list of dictionary containing:
            id: ObjectId,
            link: str
            title: str
            topic: str
            summary: str
            total_loves: int
            total_clicks: int
        '''
        
        # links = []
        
        # # get user's reco links
        # if user_id:
        #     links = (await self.get_links(db, length=length, user_id=user_id))['links']

        try:
            # recommendations = db[self.collection].aggregate([
            #     # unravel all recos
            #     {
            #         '$unwind': '$recommendations'
            #     },

            #     # filter by topic, if given
            #     {
            #         '$match': {'recommendations.topic': topic} if topic else {}
            #     },

            #     # filter by links sent to user's recos, if given
            #     {
            #         '$match': {'recommendations.link': {'$in': links}} if user_id else {}
            #     },
                
            #     # bring embdded recos to top level
            #     {
            #         '$replaceRoot': 
            #         {
            #             'newRoot': '$recommendations'
            #         }
            #     },
                
            #     # reduce only to unique recos
            #     {
            #         '$group': 
            #         {
            #             '_id': 
            #             {
            #                 'link': '$link',
            #                 'topic': '$topic',
            #                 'title': '$title',
            #                 'summary': '$summary' 
            #             },
            #             'total_loves': 
            #             {
            #                 '$sum': 
            #                 {
            #                     '$cond': ['$loved', 1, 0]
            #                 }
            #             },
            #             'total_clicks': {'$sum': '$clicks'}
            #         }
            #     },

            #     # show specific fields
            #     {
            #         '$project':
            #         {
            #             '_id': 0,
            #             'link': '$_id.link',
            #             'topic': '$_id.topic',
            #             'title': '$_id.title',
            #             'summary': '$_id.summary',
            #             'total_loves': 1,
            #             'total_clicks': 1,
            #         }
            #     }
            # ])

            articles = db.articles.find({})

            articles = await articles.to_list(length)

            return articles
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500, 
                detail="An error occured while fetching articles."
            )
    

    async def get_recommendations(self, db: AsyncIOMotorDatabase, length, user_id, topic=None):
        '''
        Get all articles recommended to user. Can be filtered by topic (optional)
        
        Returns a list of dictionary containing:
            id: ObjectId,
            link: str
            title: str
            topic: str
            summary: str
            total_clicks: int
            loved: bool
        '''
        
        try:
            
            recommendations = db[self.collection].aggregate(
                [
                    # filter only to the user
                    {
                        '$match': {'_id': ObjectId(user_id)}
                    },
                    # unwind
                    {
                        '$unwind': '$recommendations'
                    },
                    # bring to top level
                    {
                        '$replaceRoot': 
                        {
                            'newRoot': '$recommendations'
                        }
                    },
                    # ### REMOVE THESE ATTRIBUTES AND THIS PIPELINE LATER 
                    {
                        '$project':
                        {
                            '_id': 0,
                            'topic': 0,
                            'title': 0,
                            'summary': 0,
                            
                        }
                    },
                    # lookup and match article deets
                    {
                        '$lookup':
                        {
                            'from': 'articles',
                            'localField': 'link',
                            'foreignField': 'link',
                            'as': 'details'
                        }
                    },
                    # bring deets up 
                    {
                        '$replaceRoot': 
                        { 
                            'newRoot': 
                            { 
                                '$mergeObjects': 
                                [ 
                                    { 
                                        '$arrayElemAt': [ "$details", 0 ] 
                                    }, 
                                    "$$ROOT" 
                                ] 
                            } 
                        }
                    },
                    {
                        '$match': { 'topic': topic } if topic else {}
                    },
                    # include in projection the total_clicks and loved
                    # remove 'details' field
                    {
                        '$project':
                        {
                            '_id': 0,
                            'details': 0,
                            'total_loves': 0,
                            'clicks': 0
                            # 'total_clicks': 1,
                            # 'loved': 1,
                        }
                    }
                ]
            )

            recommendations = await recommendations.to_list(length)

            return recommendations
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500, 
                detail="An error occured while fetching recommendations."
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
            
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail="An error occured while updating loves." + '\n' + str(e) + '\n' + str(article) + link
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



    async def get_links(
        self,
        db: AsyncIOMotorDatabase,
        length: int,
        user_id: str
    ):
        '''
            Get links of articles recommended for the user
        '''
        user_id = ObjectId(user_id)

        try:
            links = db[self.collection].aggregate([
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
                        '_id': '$link'
                    }
                }
            ])

            links = await links.to_list(length)
            
            links_list = {'links': []}

            for link in links:
                links_list['links'].append(link['_id'])
            
            return links_list
        
        except Exception as e:
            raise HTTPException(
                status_code=404, 
                detail="An error occured while fetching topics."
            )
        

      

article = CRUDArticle('users')
