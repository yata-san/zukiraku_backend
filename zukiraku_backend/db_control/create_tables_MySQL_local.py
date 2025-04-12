import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine

# パス設定：親ディレクトリをsys.pathに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_control.mymodels_MySQL import (
    Base, User, ToDo, ToBe, ReviewSession,
    ToDoScore, ToBeScore, Answer, Question,
    Choice, ChoiceScore, ScreeningResultHistory, ScreeningResultMaster,
    Feedback
)

# 👇 モデルを強制的に読み込ませることで、テーブル作成対象として認識させる
_ = [
    User, ToDo, ToBe, ReviewSession, ToDoScore, ToBeScore,
    Answer, Question, Choice, ChoiceScore,
    ScreeningResultHistory, ScreeningResultMaster,
    Feedback
]

# .env読み込み
load_dotenv()

# 環境変数からDB接続情報を取得
DB_ENGINE = os.getenv("DB_ENGINE")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"{DB_ENGINE}+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print("🌱 ローカル接続URL:", DATABASE_URL)

# エンジン作成
engine = create_engine(DATABASE_URL)

if __name__ == "__main__":
    # ローカルDBを一度削除してから再作成
    Base.metadata.drop_all(engine)
    print("🧹 既存テーブル削除完了")

    Base.metadata.create_all(engine)
    print("✅ ローカルDB：全テーブル作成完了")
