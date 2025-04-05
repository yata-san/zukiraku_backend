import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_control.crud import myinsert
from db_control.connect_MySQL import engine
from db_control.mymodels_MySQL import User
from sqlalchemy.orm import sessionmaker

# 仮のユーザーデータ
user_data = [
    {"email": "test1@example.com", "password": "password1", "screening_type_id": "type_001"},
    {"email": "test2@example.com", "password": "password2", "screening_type_id": "type_002"},
    {"email": "admin@example.com", "password": "adminpass", "screening_type_id": "type_003"},
]

# セッション作成
Session = sessionmaker(bind=engine)
session = Session()

for user in user_data:
    existing = session.query(User).filter_by(email=user["email"]).first()
    if existing:
        print(f"スキップ：{user['email']}")
    else:
        myinsert(User, user)
        print(f"登録完了：{user['email']}")

session.close()
