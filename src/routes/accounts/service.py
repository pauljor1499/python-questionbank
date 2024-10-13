from fastapi import HTTPException
from bson import ObjectId
from typing import Optional, Type
from src.connection import SCHOOL_DATABASE
from src.routes.question_bank.models import QuestionUpdate, QuestionBase
from src.routes.question_bank.utilities.helpers import question_serializer, question_type_map
from datetime import datetime, timezone


class AccountsService:
    def __init__(self):
        if SCHOOL_DATABASE is not None:
            self.collection = SCHOOL_DATABASE["users"]
        else:
            print(f"\033[31mERROR: Unable to connect to the database.\033[0m")
            

    async def create_question(self, question_data: QuestionBase) -> dict:
        try:
            questionType = question_data["questionType"]
            print(question_data)
            if questionType not in question_type_map:
                raise HTTPException(status_code=400, detail="Invalid question type")
            QuestionModel: Type = question_type_map[questionType]
            question = QuestionModel(**question_data)
            question_dict = question.dict()
            result = await self.collection.insert_one(question_dict)
            new_question = await self.fetch_question(str(result.inserted_id))
            return {"new_question": new_question}
        except HTTPException as error:
            raise error
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while creating the question")


    async def fetch_question(self, question_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(question_id):
            raise HTTPException(status_code=400, detail="Invalid question ID format")
        try:
            question = await self.collection.find_one({"_id": ObjectId(question_id), "deleted": False})
            if not question:
                raise HTTPException(status_code=404, detail="Question not found")
            return question_serializer(question)
        except HTTPException as error:
            raise error
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while fetching the question")


    async def update_question(self, question_id: str, updated_question: QuestionUpdate) -> Optional[dict]:
        if not ObjectId.is_valid(question_id):
            raise HTTPException(status_code=400, detail="Invalid question ID format")
        # Filter out None values from updated_question
        question_data = {k: v for k, v in updated_question.model_dump().items() if v is not None}
        existing_question = await self.fetch_question(question_id)
        if existing_question is None:
            raise HTTPException(status_code=404, detail="Question not found")
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(question_id)},
                {"$set": question_data}
            )
            updated_question = await self.fetch_question(question_id) if result.modified_count > 0 else None
            return {"updated_question": updated_question}
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while updating the question")


    async def delete_question(self, question_id: str) -> dict:
        if not ObjectId.is_valid(question_id):
            raise HTTPException(status_code=400, detail="Invalid question ID format")
        question = await self.fetch_question(question_id)
        if question is None:
            raise HTTPException(status_code=404, detail="Question not found")
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(question_id)},
                {"$set": {"deleted": True, "deletedDate": datetime.now(timezone.utc)}}
            )
            if result.modified_count == 0:
                raise HTTPException(status_code=404, detail="Question not found")
            return {"deleted": True, "data": question}
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while deleting the question")