from fastapi import Request, APIRouter
from src.service import QuestionService
from src.models import QuestionUpdate


router = APIRouter()

question_service = QuestionService()

@router.get("", response_model=dict)
async def fetch_questions(request: Request) -> dict:
    query = dict(request.query_params)
    return await question_service.fetch_questions(query)

@router.post("/create", response_model=dict)
async def create_question(question_data: dict) -> dict:
    return await question_service.create_question(question_data)

@router.get("/{question_id}", response_model=dict)
async def fetch_question(question_id: str) -> dict:
    return await question_service.fetch_question(question_id)

@router.put("/update/{question_id}", response_model=dict)
async def update_question(question_id: str, updated_data: QuestionUpdate) -> dict:
    return await question_service.update_question(question_id, updated_data)

@router.delete("/delete/{question_id}", response_model=dict)
async def delete_question(question_id: str) -> dict:
    return await question_service.delete_question(question_id)