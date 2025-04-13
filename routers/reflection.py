from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, timezone, date
from openai import OpenAI
from decouple import config

# ✅ LangChain用に追加
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.schema import SystemMessage, HumanMessage

# データベース接続（Azure用）
from db_control.connect_MySQL_azure import get_db
from db_control.mymodels_MySQL import ReviewSession, ToDoScore, ToBeScore, Feedback, ToDo, ToBe

router = APIRouter()

# --- LangChainモデル初期化 ---
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7,
    openai_api_key=config("OPENAI_API_KEY")
)

# --- Pydantic モデル ---
class ToDoScoreItem(BaseModel):
    to_do_id: int
    to_do_score: int

class ToBeScoreItem(BaseModel):
    to_be_id: int
    to_be_score: int

class ReflectionRequest(BaseModel):
    user_id: int
    to_do_scores: List[ToDoScoreItem]
    to_be_scores: List[ToBeScoreItem]
    feedback_text: str

class ToDoLabelRequest(BaseModel):
    user_id: int
    to_do_ids: List[int]

class ToBeLabelRequest(BaseModel):
    user_id: int
    to_be_ids: List[int]

# --- LangChain版 応答生成関数 ---
def generate_ai_feedback_with_history(
    feedback_text, to_do_scores, to_be_scores, past_messages: list[str]
):
    history = ChatMessageHistory()
    
    # 過去の振り返り内容を履歴として追加
    for past in past_messages:
        history.add_user_message(past)

    # システムプロンプト
    history.add_message(SystemMessage(content="あなたは優しいメンタルコーチです。"))

    # 現在のプロンプト
    prompt = f"""
ユーザーの振り返りに対して、前向きなフィードバックと改善アドバイスを300文字程度で出力してください。

【振り返り内容】
{feedback_text}

【ToDoスコア】
{[f"ID:{item.to_do_id} → スコア:{item.to_do_score}" for item in to_do_scores]}

【ToBeスコア】
{[f"ID:{item.to_be_id} → スコア:{item.to_be_score}" for item in to_be_scores]}
    """
    history.add_message(HumanMessage(content=prompt))

    response = llm(history.messages)
    return response.content

# --- エンドポイント ---
@router.post("/submit_review")
def submit_review(body: ReflectionRequest, db: Session = Depends(get_db)):
    # 1. ReviewSession 作成
    review_session = ReviewSession(
        user_id=body.user_id,
        execution_date=date.today(),
        status="completed",
        created_at=datetime.now(timezone.utc)
    )
    db.add(review_session)
    db.commit()
    db.refresh(review_session)

    # 2. ToDoスコアを登録
    for item in body.to_do_scores:
        todo_score = ToDoScore(
            session_id=review_session.session_id,
            to_do_id=item.to_do_id,
            to_do_score=item.to_do_score
        )
        db.add(todo_score)

    # 3. ToBeスコアを登録
    for item in body.to_be_scores:
        tobe_score = ToBeScore(
            session_id=review_session.session_id,
            to_be_id=item.to_be_id,
            to_be_score=item.to_be_score
        )
        db.add(tobe_score)

    # 4. ユーザーの過去フィードバック履歴を取得（最大3件）
    past_feedbacks = db.query(Feedback).filter(
        Feedback.user_id == body.user_id
    ).order_by(Feedback.created_at.desc()).limit(3).all()
    past_messages = [f.feedback_text for f in past_feedbacks if f.feedback_text]

    # 5. フィードバック登録
    feedback = Feedback(
        user_id=body.user_id,
        session_id=review_session.session_id,
        feedback_text=body.feedback_text,
        created_at=datetime.now(timezone.utc)
    )
    db.add(feedback)

    # 6. LangChainを使ってAIフィードバックを生成
    ai_feedback = generate_ai_feedback_with_history(
        feedback_text=body.feedback_text,
        to_do_scores=body.to_do_scores,
        to_be_scores=body.to_be_scores,
        past_messages=past_messages
    )
    feedback.ai_feedback = ai_feedback

    db.commit()

    return {
        "message": "Review submitted successfully",
        "ai_feedback": ai_feedback
    }

@router.post("/get_to_do_labels")
def get_to_do_labels(body: ToDoLabelRequest, db: Session = Depends(get_db)):
    result = db.query(ToDo).filter(
        ToDo.user_id == body.user_id,
        ToDo.to_do_id.in_(body.to_do_ids)
    ).all()
    return {item.to_do_id: item.label for item in result}

@router.post("/get_to_be_labels")
def get_to_be_labels(body: ToBeLabelRequest, db: Session = Depends(get_db)):
    result = db.query(ToBe).filter(
        ToBe.user_id == body.user_id,
        ToBe.to_be_id.in_(body.to_be_ids)
    ).all()
    return {item.to_be_id: item.label for item in result}
