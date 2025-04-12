from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

# Azure接続情報
DATABASE_URL = "mysql+pymysql://tech0gen9student:vY7JZNfU@rdbs-002-step3-2-oshima1.mysql.database.azure.com:3306/crm_mysql"

if os.path.exists("/home/site/wwwroot/DigiCertGlobalRootCA.crt.pem"):
    SSL_CA_PATH = "/home/site/wwwroot/DigiCertGlobalRootCA.crt.pem"
else:
    SSL_CA_PATH = "C:/Users/herim/Desktop/Tech0/zukiraku_backend/DigiCertGlobalRootCA.crt.pem"

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
