# scripts/reset_and_seed.py

import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from db_control.connect_MySQL import engine
from db_control import mymodels_MySQL as models
from sqlalchemy.orm import sessionmaker

from insert_data import (
    insert_questions,
    insert_choices,
    insert_choice_scores,
)

# セッション作成
Session = sessionmaker(bind=engine)
session = Session()

def reset_database():
    print("⚠️  既存テーブルを全削除します...")
    models.Base.metadata.drop_all(bind=engine)
    print("✅ テーブル削除完了")

    print("🛠 テーブルを再作成します...")
    models.Base.metadata.create_all(bind=engine)
    print("✅ テーブル作成完了")

def insert_initial_data():
    print("\n🚀 初期データを挿入します...")
    insert_questions.run(session)
    insert_choices.run(session)
    insert_choice_scores.run(session)
    print("✅ 初期データの挿入完了")

if __name__ == "__main__":
    reset_database()
    insert_initial_data()
    session.close()
