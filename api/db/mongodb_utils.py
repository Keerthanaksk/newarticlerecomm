from api.db.mongodb import db
from api.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

async def connect_to_mongo():
    # logging.info("Connecting to MongoDB client and db...")

    MONGO_URL = settings.MONGO_URL
    MONGO_DB = settings.MONGO_DB
    
    db.client = AsyncIOMotorClient(MONGO_URL)
    db.db = db.client[MONGO_DB]

    # logging.info("Connected to MongoDB client and db!")



async def close_mongo_connection():
    # logging.info("Closing MongoDB client...")
    db.client.close()
    # logging.info("Connection to MongoDB client closed.")