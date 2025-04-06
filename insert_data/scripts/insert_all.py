# insert_all.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy.orm import sessionmaker
from db_control.connect_MySQL import engine

# 各データ挿入スクリプトの import
from insert_data.scripts import (
    insert_questions,
    insert_choices,
    insert_choice_scores,
    insert_answers,
    insert_screening_types,
    insert_screening_results,
    insert_users
)

Session = sessionmaker(bind=engine)
session = Session()

def insert_all():
    try:
        print("\n🔄 insert_questions 開始...")
        insert_questions.run(session)

        print("\n🔄 insert_choices 開始...")
        insert_choices.run(session)

        print("\n🔄 insert_choice_scores 開始...")
        insert_choice_scores.run(session)

        print("\n🔄 insert_answers 開始...")
        insert_answers.run(session)

        print("\n🔄 insert_screening_types 開始...")
        insert_screening_types.run(session)

        print("\n🔄 insert_screening_results 開始...")
        insert_screening_results.run(session)

        print("\n🔄 insert_users 開始...")
        insert_users.run(session)

        print("\n✅ すべての初期データを挿入しました。")

    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        session.rollback()

    finally:
        session.close()
        print("🔚 セッションを終了しました。")

if __name__ == "__main__":
    insert_all()