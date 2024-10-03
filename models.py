from pydantic import BaseModel, Field
from typing import List, Optional, Union

class Choice(BaseModel):
    id: int
    text: Optional[str] = None

class Answer(BaseModel):
    id: int
    answer: str  # This should be a string

class CorrectAnswer(BaseModel):
    answers: Union[List[Answer], List[str], str]  # Can be a list of Answer objects, a list of strings, or a single string
    answerDetails: Optional[str] = None

class Question(BaseModel):
    question: str
    choices: Optional[List[Choice]] = None  # Choices can be null or a list
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
