from pydantic import BaseModel, Field
from typing import List, Optional, Union

class Item(BaseModel):
    id: int # custom ID
    text: str

class Choice(BaseModel):
    id: int # custom ID
    items: List[Item]  # List of items for drop-down-menu type

class Answer(BaseModel):
    id: int  # custom ID
    answer: str  # Actual answer text

class CorrectAnswer(BaseModel):
    answers: Union[List[Answer], List[str], str] # Can be a list of Answer objects, a list of strings, or a single string
    answerDetails: Optional[str] = None

class Question(BaseModel):
    question: str  # The main question text
    choices: Optional[List[Union[Item, Choice]]] = None  # Choices can be None/null for free-response/graph
    correctAnswer: CorrectAnswer  # Correct answers with details
    questionDetails: Optional[str] = None
    assignmentType: str  # Type of assignment (STAAR, SAT, ACT, TSI)
    questionType: str  # Type of question (Multiple-choice, Checkbox, Free-response, Graph, Drop-down-Menu, Drag-and-drop)
    difficulty: Optional[str] = None
    teksCode: Optional[str] = None
    points: str

class QuestionUpdate(BaseModel):
    question: Optional[str] = None
    choices: Optional[List[Union[Item, Choice]]] = None
    correctAnswer: Optional[CorrectAnswer] = None
    questionDetails: Optional[str] = None
    assignmentType: Optional[str] = None
    questionType: Optional[str] = None
    difficulty: Optional[str] = None
    teksCode: Optional[str] = None
    points: Optional[str] = None
