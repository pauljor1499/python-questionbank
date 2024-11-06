from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.connection import init_master_db
from contextlib import asynccontextmanager
from src.routes.question_bank.question_bank import router as QuestionBank


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_master_db()
    yield

app = FastAPI(
    title="Analytics Bank",
    description="Owned by: EruditionTx Team",
    version="Version 1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Server is up and running."}

app.include_router(QuestionBank, tags=["Questions"], prefix="/questions")