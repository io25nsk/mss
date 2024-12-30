from motor.motor_asyncio import AsyncIOMotorClient

from settings import settings


DB_URI = f"{settings.DB_PREFIX}://{settings.DB_HOST}:{settings.DB_PORT}/"
CLIENT = AsyncIOMotorClient(DB_URI)
DB = CLIENT.mss
USERS_COLLECTION = DB.users
