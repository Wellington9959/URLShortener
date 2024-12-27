from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings

db = AsyncIOMotorClient(settings.MONGO_URI).shortenerDB
