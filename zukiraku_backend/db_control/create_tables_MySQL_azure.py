import sys
import os
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

# Azure接続URL（固定）
DATABASE_URL = (
    "mysql+pymysql://tech0gen9student:vY7JZNfU@rdbs-002-step3-2-oshima1.mysql.database.azure.com:3306/crm_mysql"
)

# SSL証明書パスを明示
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": "C:/Users/herim/Desktop/DigiCertGlobalRootCA.crt.pem"
        }
    }
)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("✅ AzureDB：全テーブル作成完了")

