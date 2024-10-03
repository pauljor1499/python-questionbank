from pydantic import BaseModel, Field
from typing import Optional

class Question(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class QuestionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
