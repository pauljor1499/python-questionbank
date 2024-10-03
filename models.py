from pydantic import BaseModel, Field
from typing import List, Optional, Union

class Item(BaseModel):
    id: int
    text: str  # Text for each item in choices (used for multiple-choice, checkbox, drop-down-menu)

class Choice(BaseModel):
    id: int
    items: List[Item]  # List of items for drop-down-menu type

class Answer(BaseModel):
    id: int  # ID for the answer
    answer: str  # Actual answer text

class CorrectAnswer(BaseModel):
    answers: Union[List[Answer], List[str], str] # Can be a list of Answer objects, a list of strings, or a single string
    answerDetails: Optional[str] = None  # Additional details about correct answers

class Question(BaseModel):
    question: str  # The main question text
    choices: Optional[List[Union[Item, Choice]]] = None  # Choices can be None for free-response/graph
    correctAnswer: CorrectAnswer  # Correct answers with details
    questionDetails: Optional[str] = None  # Additional question details
    assignmentType: str  # Type of assignment (e.g., TSI)
    questionType: str  # Type of question (e.g., Multiple-choice, Checkbox, Drop-down-Menu, Drag-and-drop)
    difficulty: Optional[str] = None  # Difficulty level
    teksCode: Optional[str] = None  # TEKS code
    points: str  # Points assigned for the question

class QuestionUpdate(BaseModel):
    question: Optional[str] = None  # To update the question text
    choices: Optional[List[Union[Item, Choice]]] = None  # To update the choices
    correctAnswer: Optional[CorrectAnswer] = None  # To update correct answers
    questionDetails: Optional[str] = None  # To update additional details
    assignmentType: Optional[str] = None  # To update assignment type
    questionType: Optional[str] = None  # To update question type
    difficulty: Optional[str] = None  # To update difficulty
    teksCode: Optional[str] = None  # To update TEKS code
    points: Optional[str] = None  # To update points
