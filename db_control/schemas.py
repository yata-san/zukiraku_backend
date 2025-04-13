# db_control/schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import date


# 回答登録用リクエストスキーマ
class AnswerCreate(BaseModel):
    session_id: str
    question_id: int
    choice_id: int
    screening_type_id: Optional[str] = None  # 任意（診断前ならnullの可能性）

# レスポンス用（必要なら）
class AnswerResponse(BaseModel):
    answer_id: int
    session_id: str
    question_id: int
    choice_id: int
    screening_type_id: Optional[str]

    class Config:
        from_attributes = True  # ✅ Pydantic v2対応  # SQLAlchemyモデル → Pydanticモデル変換を許可

class ScoreItem(BaseModel):
    to_be_id: int
    score: int

class HabitItem(BaseModel):
    to_do_id: int
    score: int

class ReviewSessionOut(BaseModel):
    session_id: str
    date: date
    comment: str
    ratings: dict

    class Config:
        from_attributes = True
