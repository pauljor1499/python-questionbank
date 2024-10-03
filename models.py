from pydantic import BaseModel, Field
from typing import List, Optional, Union

class Choice(BaseModel):
    id: int
    text: Optional[str] = None
    # choice: Optional[str] = None  # Used for Free-response questions

class CorrectAnswer(BaseModel):
    answers: Union[List[str], str]  # Adjusted to handle both lists and single string
    answerDetails: Optional[str] = None

class Question(BaseModel):
    # id: int
    question: str
    choices: Optional[List[Choice]]
    correctAnswer: CorrectAnswer
    questionDetails: Optional[str] = None
    assignmentType: str
    questionType: str
    difficulty: Optional[str] = None
    teksCode: Optional[str] = None
    points: str

class QuestionUpdate(BaseModel):
    question: Optional[str] = None
    choices: Optional[List[Choice]] = None
    correctAnswer: Optional[CorrectAnswer] = None
    questionDetails: Optional[str] = None
    assignmentType: Optional[str] = None
    questionType: Optional[str] = None
    difficulty: Optional[str] = None
    teksCode: Optional[str] = None
    points: Optional[str] = None
