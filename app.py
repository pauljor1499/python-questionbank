from fastapi import FastAPI, HTTPException, Query
from models import Question, QuestionUpdate
from question_service import QuestionService
from typing import Optional

app = FastAPI()

db_url = "mongodb+srv://admin:admin@cluster0.aeltnpt.mongodb.net/"
question_service = QuestionService(db_url)

# Create a question
@app.post("/questions/create")
async def create_question(question: Question):
    question_data = question.model_dump()
    question_id = await question_service.create_question(question_data)
    return {"id": question_id}

# Get a single question by ID
@app.get("/questions/{question_id}")
async def fetch_question(question_id: str):
    question = await question_service.fetch_question(question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

# Update a question by ID
@app.put("/questions/{question_id}")
async def update_question(question_id: str, question_update: QuestionUpdate):
    updated_data = {k: v for k, v in question_update.model_dump().items() if v is not None}
    if not await question_service.fetch_question(question_id):
        raise HTTPException(status_code=404, detail="Question not found")
    await question_service.update_question(question_id, updated_data)
    return {"msg": "Question updated"}

# Delete a question by ID
@app.delete("/questions/{question_id}")
async def delete_question(question_id: str):
    if not await question_service.delete_question(question_id):
        raise HTTPException(status_code=404, detail="Question not found")
    return {"msg": "Question deleted"}

# Fetch all questions
@app.get("/questions/")
async def fetch_questions(price: Optional[float] = Query(None)):
    questions = await question_service.fetch_questions(price)
    return questions