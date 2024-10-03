from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

def question_serializer(question) -> dict:
    return {
        "_id": str(question["_id"]),
        "name": question["name"],
        "description": question.get("description"),
        "price": question["price"],
        "stock": question["stock"]
    }

class QuestionService:
    def __init__(self, db_client: str):
        self.client = AsyncIOMotorClient(db_client)
        self.db = self.client["teacher-questionbank"]
        self.collection = self.db["questionbank"]

    # Create a question
    async def create_question(self, question_data: dict):
        result = await self.collection.insert_one(question_data)
        return str(result.inserted_id)

    # Get a single question by ID
    async def fetch_question(self, question_id: str):
        question = await self.collection.find_one({"_id": ObjectId(question_id)})
        if question:
            return question_serializer(question)
        return None

    # Update a question by ID
    async def update_question(self, question_id: str, question_data: dict):
        result = await self.collection.update_one({"_id": ObjectId(question_id)}, {"$set": question_data})
        if result.modified_count:
            question = await self.fetch_question(question_id)
            return question
        return None

    # Delete a question by ID
    async def delete_question(self, question_id: str):
        result = await self.collection.delete_one({"_id": ObjectId(question_id)})
        return result.deleted_count > 0

    # Fetch all question
    async def fetch_questions(self, price: float = None):
        pipeline = []
        if price is not None:
            pipeline.append({
                "$match": {"price": price}  # Add price filter if provided
            })
        questions = await self.collection.aggregate(pipeline).to_list(100)  # Awaiting async aggregation and limiting to 100
        return [question_serializer(question) for question in questions]
