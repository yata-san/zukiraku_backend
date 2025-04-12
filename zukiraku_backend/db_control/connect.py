from sqlalchemy import create_engine
# import sqlalchemy

# db_control/connect.py
from sqlalchemy.orm import sessionmaker
from db_control.connect_MySQL import engine
from sqlalchemy.orm import Session
from fastapi import Depends

import os
# uname() error回避
import platform
print("platform:", platform.uname())

# セッション生成器（共通で使いまわす）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

main_path = os.path.dirname(os.path.abspath(__file__))
path = os.chdir(main_path)
print("path:", path)
engine = create_engine("sqlite:///CRM.db", echo=True)

# FastAPI の Depends で使えるDBセッション
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()