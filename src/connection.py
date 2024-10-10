from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv
import os
from src.models import (
    QuestionBase, QuestionUpdate
)

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://admin:admin@cluster0.aeltnpt.mongodb.net/") # "mongodb+srv://admin:admin@cluster0.aeltnpt.mongodb.net/"
DB_NAME = os.getenv("DB_NAME", "teacher-questionbank")
client = AsyncIOMotorClient(MONGO_URL)

async def init_db():
    try:
        await init_beanie(
            database=client[DB_NAME],
            document_models=[
                QuestionBase,
                QuestionUpdate,
            ],
        )
    except Exception as e:
        print(e)