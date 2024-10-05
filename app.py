from fastapi import FastAPI, HTTPException, Query
from models import Question, QuestionUpdate
from question_service import QuestionService
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


db_url = "mongodb+srv://admin:admin@cluster0.aeltnpt.mongodb.net/"
question_service = QuestionService(db_url)


@app.post("/questions/create", response_model=dict)
async def create_question(question: Question) -> dict:
    """Create a new question."""
    question_data = question.model_dump()
    question_id = await question_service.create_question(question_data)
    return {"new_question": question_id}


@app.get("/questions/{question_id}", response_model=dict)
async def fetch_question(question_id: str) -> dict:
    """Fetch a single question by its ID."""
    question = await question_service.fetch_question(question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@app.put("/questions/update/{question_id}", response_model=dict)
async def update_question(question_id: str, question_update: QuestionUpdate) -> dict:
    """Update a question by its ID."""
    updated_data = {k: v for k, v in question_update.model_dump().items() if v is not None}
    if not await question_service.fetch_question(question_id):
        raise HTTPException(status_code=404, detail="Question not found")
    updated_question = await question_service.update_question(question_id, updated_data)
    return {"data": updated_question}


@app.delete("/questions/delete/{question_id}", response_model=dict)
async def delete_question(question_id: str) -> dict:
    """Delete a question by its ID."""
    question = await question_service.delete_question(question_id)
    if not question["deleted"]:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"data": question}


@app.get("/questions", response_model=dict)
async def fetch_questions(question_type: Optional[str] = Query(None), 
    assignment_type: Optional[str] = Query(None), 
    category: Optional[str] = Query(None), 
    difficulty: Optional[str] = Query(None), 
    page: int = Query(1, gt=0),  # Defaults to 1, must be greater than 0
    page_size: int = Query(10, gt=0, le=100)  # Defaults to 10, with a max of 100
) -> dict:
    """Fetch all questions, optionally filtered with pagination."""
    try:
        questions = await question_service.fetch_questions(
            question_type=question_type, 
            assignment_type=assignment_type, 
            category=category, 
            difficulty=difficulty, 
            page=page, 
            page_size=page_size
        )
        return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching questions: {e}")
