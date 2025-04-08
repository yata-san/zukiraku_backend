# insert_screening_types.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_control.mymodels_MySQL import ScreeningType
from db_control.crud import myinsert

# スクリーニングタイプの初期データ
screening_types = [
    {"screening_type_id": f"type_{i:03d}"} for i in range(1, 8)
]

def run(session):
    for row in screening_types:
        existing = session.query(ScreeningType).filter_by(screening_type_id=row["screening_type_id"]).first()
        if existing:
            print(f"スキップ：{row['screening_type_id']}")
        else:
            myinsert(ScreeningType, row)
            print(f"登録：{row['screening_type_id']}")

# 単体実行用
if __name__ == "__main__":
    from sqlalchemy.orm import sessionmaker
    from db_control.connect_MySQL import engine
    Session = sessionmaker(bind=engine)
    session = Session()
    run(session)
    session.close()
