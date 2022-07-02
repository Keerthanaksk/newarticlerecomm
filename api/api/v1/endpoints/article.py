
@app.get("/")
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



@app.get("/{id}")
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



@app.patch("/loves/{id}")
async def increment_loves_by_id(id):
    oid = ObjectId(id)
    
    await coll.update_one({'_id': oid}, {'$inc': {'loves': 1}})
    
    article = await coll.find_one({'_id': oid})

    article = {
        'id': str(article['_id']), 
        'loves': article['loves']
    }

    return article



@app.patch("/clicks/{id}")
async def increment_clicks_by_id(id):
    '''
        Sets clicked to true (1) and increments clicks
    '''
    
    oid = ObjectId(id)
    
    await coll.update_one({'_id': oid}, {'$inc': {'clicks': 1}, '$set' : {'clicked': True}})
    
    # return 200
    return 1