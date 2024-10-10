from fastapi import HTTPException
from bson import ObjectId
from typing import Optional, Type
from src.connection import DB_NAME, client
from src.models import QuestionUpdate
from src.utilities import question_serializer, question_type_map


class QuestionService:
    def __init__(self):
        self.client = client
        self.db = self.client[DB_NAME]
        self.collection = self.db["questionbank"]
        if self.client is None:
            print("\033[31mUnable to connect from the Database.\033[0m")
        else:
            print("\033[32mSuccessfully connected from the Database.\033[0m")


    async def create_question(self, question_data: dict) -> dict:
        try:
            questionType = question_data["questionType"]
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
                {"$set": {"deleted": True}}
            )
            if result.modified_count == 0:
                raise HTTPException(status_code=404, detail="Question not found")
            return {"deleted": True, "data": question}
        except Exception as e:
            print(f"\033[31mERROR: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Error while deleting the question")


    async def fetch_questions(self, query: dict) -> dict:
        question_type = query.get("questionType", None)
        assignment_type = query.get("assignmentType", None)
        category = query.get("category", None)
        difficulty = query.get("difficulty", None)
        page = query.get("page", 1)
        page_size = query.get("page_size", 10)

        skip = (page - 1) * page_size
        limit = page_size

        match_criteria = {"deleted": False}
        
        if question_type:
            match_criteria["questionType"] = question_type
        if assignment_type:
            match_criteria["assignmentType"] = assignment_type
        if category:
            match_criteria["category"] = category
        if difficulty:
            match_criteria["difficulty"] = difficulty

        # Count total questions that match the criteria
        total_questions = await self.collection.count_documents(match_criteria)

        # Create the aggregation pipeline for counting groupings
        pipeline = []

        if match_criteria:
            pipeline.append({"$match": match_criteria})

        # Create the aggregation pipeline for counting groupings
        pipeline.append({
            "$group": {
                "_id": {
                    "assignmentType": "$assignmentType",
                    "questionType": "$questionType",
                    "category": "$category",
                    "difficulty": "$difficulty"
                },
                "count": {"$sum": 1}
            }
        })

        try:
            counts = await self.collection.aggregate(pipeline).to_list(100)
            assignment_types_counts = {"STAAR": 0, "TSI": 0, "SAT": 0, "ACT": 0}
            question_types_counts, categories_counts, difficulties_counts = {}, {}, {}

            for item in counts:
                assignment_type = item["_id"]["assignmentType"]
                question_type = item["_id"]["questionType"]
                category = item["_id"]["category"]
                difficulty = item["_id"]["difficulty"]
                count = item["count"]

                if assignment_type in assignment_types_counts:
                    assignment_types_counts[assignment_type] += count
                if question_type:
                    question_types_counts[question_type] = question_types_counts.get(question_type, 0) + count
                if category:
                    categories_counts[category] = categories_counts.get(category, 0) + count
                if difficulty:
                    difficulties_counts[difficulty] = difficulties_counts.get(difficulty, 0) + count

        except Exception as e:
            print(f"Error counting assignment types, question types, categories, or difficulties: {e}")
            assignment_types_counts = {key: 0 for key in assignment_types_counts}
            question_types_counts, categories_counts, difficulties_counts = {}, {}, {}

        # Fetch questions with pagination
        questions_pipeline = []

        if match_criteria:
            questions_pipeline.append({"$match": match_criteria})

        questions_pipeline.append({"$skip": skip})
        questions_pipeline.append({"$limit": limit})

        try:
            questions = await self.collection.aggregate(questions_pipeline).to_list(100)
            question_list = [question_serializer(question) for question in questions]
        except Exception as e:
            print(f"Error fetching questions: {e}")
            question_list = []

        return {
            "data": {
                "questions": question_list,
                "assignmentTypes": assignment_types_counts,
                "questionTypes": question_types_counts,
                "categories": categories_counts,
                "difficulties": difficulties_counts,
            },
            "pagination": {
                "page": page,
                "pageSize": page_size,
                "totalCount": len(question_list),
                "totalQuestions": total_questions
            }
        }
