from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

# Azure接続情報
DATABASE_URL = "mysql+pymysql://tech0gen9student:vY7JZNfU@rdbs-002-step3-2-oshima1.mysql.database.azure.com:3306/crm_mysql"

# SSL証明書のパスを環境変数から取得、なければローカルパスを fallback に
SSL_CA_PATH = os.getenv("SSL_CA", "C:/Users/herim/Desktop/Tech0/zukiraku_backend/DigiCertGlobalRootCA.crt.pem")

engine = create_engine(
    DATABASE_URL,
    connect_args={"ssl": {"ca": SSL_CA_PATH}}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
