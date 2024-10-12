from motor.motor_asyncio import AsyncIOMotorClient
# from beanie import init_beanie
import os


MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://admin:admin@cluster0.aeltnpt.mongodb.net/") # "mongodb+srv://admin:admin@cluster0.aeltnpt.mongodb.net/"
DB_NAME = os.getenv("DB_NAME", "teacher-questionbank")
DB_CLIENT = AsyncIOMotorClient(MONGO_URL)
DATABASE = DB_CLIENT[DB_NAME]

async def init_db():
    try:
        collections = await DATABASE.list_collection_names()
        print(f"\033[32mINFO: Connected to the database: [{DB_NAME}], collections: {collections}\033[0m")
    except Exception as e:
        print(f"\033[31mERROR: Unable to connect to the database.\033[0m")
        print(f"\033[31mERROR: {e}\033[0m")