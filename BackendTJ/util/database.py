from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine, ObjectId


class Database:

    def __init__(self, url, name):
        client = AsyncIOMotorClient(url)
        self.engine = AIOEngine(motor_client=client, database=name)
