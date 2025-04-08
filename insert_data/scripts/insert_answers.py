import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_control.crud import myinsert
from db_control.mymodels_MySQL import User, Question, Choice, Answer

def run(session):
    # 対象ユーザーを1人取得（今回は test1@example.com）
    user = session.query(User).filter_by(email="test1@example.com").first()
    if not user:
        print("❌ ユーザーが見つかりません")
        return

    # 質問（最初の10問）取得
    questions = session.query(Question).order_by(Question.question_id).limit(10).all()

    for question in questions:
        # 選択肢を取得
        choices = session.query(Choice).filter_by(question_id=question.question_id).all()
        if not choices:
            print(f"⚠️ 選択肢なし: question_id={question.question_id}")
            continue

        # ランダムに1つ選ぶ
        selected_choice = random.choice(choices)

        # 重複チェック
        existing = session.query(Answer).filter_by(
            screening_type_id=user.screening_type_id,
            question_id=question.question_id,
            choice_id=selected_choice.choice_id
        ).first()

        if existing:
            print(f"スキップ：Q{question.question_id} に既に回答あり")
        else:
            myinsert(Answer, {
                "screening_type_id": user.screening_type_id,
                "question_id": question.question_id,
                "choice_id": selected_choice.choice_id
            })
            print(f"登録完了：Q{question.question_id} → 選択肢 {selected_choice.label}")

# 単体実行用
if __name__ == "__main__":
    from sqlalchemy.orm import sessionmaker
    from db_control.connect_MySQL import engine
    Session = sessionmaker(bind=engine)
    session = Session()
    run(session)
    session.close()
