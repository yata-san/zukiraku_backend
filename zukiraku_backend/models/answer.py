# models/answer.py

from pydantic import BaseModel
from typing import List

class AnswerItem(BaseModel):
    question_id: int
    choice_id: int

class AnswerRequest(BaseModel):
    session_id: str  # ← 復活
    answers: List[AnswerItem]

class AnswerCreate(BaseModel):
    screening_type_id: str
    session_id: str
    question_id: int
    choice_id: int
