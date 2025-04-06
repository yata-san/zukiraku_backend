# uname() error回避
import platform
print("platform", platform.uname())


from sqlalchemy import create_engine, insert, delete, update, select
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
import json
import pandas as pd
import uuid

from db_control.connect_MySQL import engine
from db_control.mymodels_MySQL import Answer, ScreeningType, ScreeningResult, ChoiceScore
from datetime import datetime
# AnswerCreate スキーマをインポート
from db_control.schemas import AnswerCreate
from models.answer import AnswerCreate  # 追加

def get_scores_by_choice_id(choice_id: int, db: Session):
    return db.query(ChoiceScore).filter(ChoiceScore.choice_id == choice_id).all()

def create_answer(answer_data: AnswerCreate, db: Session):
    answer = Answer(
        screening_type_id=answer_data.screening_type_id,
        session_id=answer_data.session_id,
        question_id=answer_data.question_id,
        choice_id=answer_data.choice_id,
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer

def generate_screening_type_id():
    return str(uuid.uuid4())

def insert_screening_type(screening_type_id: str, created_at: datetime, db: Session):
    screening_type = ScreeningType(screening_type_id=screening_type_id, created_at=created_at)
    db.add(screening_type)
    db.commit()

def insert_screening_result(screening_type_id: str, headache_type: str, scores: dict, diagnosed_at: datetime, db: Session):
    result = ScreeningResult(
        screening_type_id=screening_type_id,
        type_id=headache_type,
        headache_type=headache_type,
        symptom="（あとで追加）",
        trigger="（あとで追加）",
        advice="（あとで追加）",
        diagnosed_at=diagnosed_at
    )
    db.add(result)
    db.commit()

def myinsert(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    query = insert(mymodel).values(values)
    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()

    # セッションを閉じる
    session.close()
    return "inserted"


def myselect(mymodel, customer_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(mymodel).filter(mymodel.customer_id == customer_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for customer_info in result:
            result_dict_list.append({
                "customer_id": customer_info.customer_id,
                "customer_name": customer_info.customer_name,
                "age": customer_info.age,
                "gender": customer_info.gender
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")

    # セッションを閉じる
    session.close()
    return result_json


def myselectAll(mymodel):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = select(mymodel)
    try:
        # トランザクションを開始
        with session.begin():
            df = pd.read_sql_query(query, con=engine)
            result_json = df.to_json(orient='records', force_ascii=False)

    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        result_json = None

    # セッションを閉じる
    session.close()
    return result_json


def myupdate(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    customer_id = values.pop("customer_id")

    #"お見事！E0002の原因はこのクエリの実装ミスです。正しく実装しましょう"
    query = update(mymodel).where(mymodel.customer_id == customer_id).values(values)
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()
    # セッションを閉じる
    session.close()
    return "put"


def mydelete(mymodel, customer_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = delete(mymodel).where(mymodel.customer_id == customer_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()

    # セッションを閉じる
    session.close()
    return customer_id + " is deleted"