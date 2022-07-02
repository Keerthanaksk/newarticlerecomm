from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

class Database:
    client: AsyncIOMotorClient = None
    db : AsyncIOMotorDatabase = None

db = Database()

async def get_database() -> AsyncIOMotorDatabase:
    return db.db