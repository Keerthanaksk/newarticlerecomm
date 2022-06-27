from typing import Optional
from fastapi import FastAPI
import motor.motor_asyncio
from bson import ObjectId
from starlette.middleware.cors import CORSMiddleware
# from fastapi.middleware.cors import CORSMiddleware

# app obj
app = FastAPI()

origins = [
    "http://localhost:8080",
    "https://nice-tree-0f2a4be10.1.azurestaticapps.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# connect to azure mongodb
url = 'mongodb://ralf-mongodb:rlTDq9VZznIYUMPauBYhAGKDbKWADg6rXlFKoOb8r3i1SNPY8XsD2b2Aad2DzRqlWND2LXTvGwf7up7JFM6Czw==@ralf-mongodb.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@ralf-mongodb@'

client = motor.motor_asyncio.AsyncIOMotorClient(url)

db = client.unionbank
coll = db.articles

@app.get("/api")
async def get_all(topic = None):
    articles = []
    cursor = coll.find({'topic':topic} if topic else {})
    
    async for article in cursor:
        articles.append(
            {
                'id': str(article['_id']), 
                'title': article['title'],
                'link': article['link'],
                'topic': article['topic'],
                'summary': article['summary'],
                'clicked': article['clicked'],
                'liked': article['liked'],
                'clicks': article['clicks'],
                'loves': article['loves']
            }
        )
    return articles



@app.get("/api/{id}")
async def get_by_id(id):
    oid = ObjectId(id)
    article = await coll.find_one({'_id': oid})
    
    article = {
        'id': str(article['_id']), 
        'link': article['link'],
        'topic': article['topic'],
        'summary': article['summary'],
        'clicked': article['clicked'],
        'liked': article['liked'],
        'clicks': article['clicks'],
        'loves': article['loves']
    }
    return article



@app.patch("/api/loves/{id}")
async def increment_loves_by_id(id):
    oid = ObjectId(id)
    
    await coll.update_one({'_id': oid}, {'$inc': {'loves': 1}})
    
    article = await coll.find_one({'_id': oid})

    article = {
        'id': str(article['_id']), 
        'loves': article['loves']
    }

    return article



@app.patch("/api/clicks/{id}")
async def increment_clicks_by_id(id):
    '''
        Sets clicked to true (1) and increments clicks
    '''
    
    oid = ObjectId(id)
    
    await coll.update_one({'_id': oid}, {'$inc': {'clicks': 1}, '$set' : {'clicked': True}})
    
    # return 200
    return 1