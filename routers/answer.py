from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, UTC

# ✅ 本番DB（Azure）への接続
from db_control.connect_MySQL_azure import get_db

# ✅ 使用するテーブル（ORMモデル）を読み込み
from db_control.mymodels_MySQL import (
    Answer,
    Choice,
    ChoiceScore,
    Question,
    ScreeningResultHistory,
    ScreeningResultMaster,
    User
)

# リクエスト/バリデーション用モデルとサービスロジック
from models.answer import AnswerRequest, AnswerCreate
from services import scoring
from db_control import crud

router = APIRouter()

@router.post("/answers")
def submit_answers(payload: AnswerRequest, db: Session = Depends(get_db)):
    # ❶ screening_type_id を生成して先に登録
    screening_type_id = crud.generate_screening_type_id()
    crud.insert_screening_type(screening_type_id, datetime.now(UTC), db)

    # ❷ 回答を保存（screening_type_id を使って）
    for item in payload.answers:
        answer_data = AnswerCreate(
            screening_type_id=screening_type_id,
            session_id=payload.session_id,
            question_id=item.question_id,
            choice_id=item.choice_id
        )
        crud.create_answer(answer_data, db)

    # ❸ スコア計算
    choice_ids = [item.choice_id for item in payload.answers]
    score_dict = scoring.calculate_scores(choice_ids, db)
    headache_type = scoring.determine_headache_type(score_dict)

    # ❹ 結果の登録
    crud.insert_screening_result(
        screening_type_id=screening_type_id,
        headache_type=headache_type,
        scores=score_dict,
        diagnosed_at=datetime.now(UTC),
        db=db
    )

    return {
        "screening_type_id": screening_type_id,
        "headache_type": headache_type,
        "scores": score_dict
    }
