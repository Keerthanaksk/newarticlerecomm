# from pymongo import MongoClient
from http import client
from pymongo import MongoClient


# client = MongoClient('localhost:27017')

# obtain article collection
class Nos:
    DB_NAME = 'test'


nos = Nos()
client = MongoClient('localhost:27017')
db = client[nos.DB_NAME]

def test():
    result = db.test.insert_one({'test':'yo'})

    return result


print(test())