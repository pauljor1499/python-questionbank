from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional

def question_serializer(question: dict) -> dict:
    return {
        "_id": str(question["_id"]),
        "question": question["question"], #required
        "choices": question.get("choices"), #optional (with get is optional)
        "correctAnswer": question["correctAnswer"],
        "questionDetails": question.get("questionDetails"),
        "assignmentType": question["assignmentType"],
        "questionType": question["questionType"],
        "difficulty": question.get("difficulty"),
        "teksCode": question["teksCode"],
        "points": question["points"]
    }

class QuestionService:
    def __init__(self, db_client: str):
        self.client = AsyncIOMotorClient(db_client)
        self.db = self.client["teacher-questionbank"]
        self.collection = self.db["questionbank"]
        if self.client is None:
            print("Failed to connect to MongoDB.")
        else:
            print("Connected to MongoDB.")

    async def create_question(self, question_data: dict) -> str:
        """Create a new question and return its ID."""
        result = await self.collection.insert_one(question_data)
        return str(result.inserted_id)

    async def fetch_question(self, question_id: str) -> Optional[dict]:
        """Fetch a single question by its ID."""
        question = await self.collection.find_one({"_id": ObjectId(question_id)})
        return question_serializer(question) if question else None

    async def update_question(self, question_id: str, question_data: dict) -> Optional[dict]:
        """Update an existing question by its ID and return the updated question."""
        result = await self.collection.update_one(
            {"_id": ObjectId(question_id)},
            {"$set": question_data}
        )
        return await self.fetch_question(question_id) if result.modified_count else None

    async def delete_question(self, question_id: str) -> bool:
        """Delete a question by its ID and return a boolean indicating success."""
        result = await self.collection.delete_one({"_id": ObjectId(question_id)})
        return result.deleted_count > 0

    async def fetch_questions(self, question_type: Optional[str] = None) -> List[dict]:
        """Fetch all questions, optionally filtered by questionType."""
        pipeline = []

        # Add match stage if question_type is provided
        if question_type is not None:
            pipeline.append({"$match": {"questionType": question_type}})

        try:
            # Perform aggregation and limit to 100 results
            questions = await self.collection.aggregate(pipeline).to_list(100)
            return [question_serializer(question) for question in questions]
        except Exception as e:
            # Handle exceptions (optional logging)
            print(f"Error fetching questions: {e}")
            return []


