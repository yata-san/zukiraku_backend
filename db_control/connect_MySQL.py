print("🚨 connect_MySQL.py が読み込まれました！")
raise RuntimeError("このファイルはもう使いません")

from sqlalchemy import create_engine
import os
from pathlib import Path
from dotenv import load_dotenv

# 環境変数の読み込み
base_path = Path(__file__).parents[1]  # backendディレクトリへのパス
env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)

# データベース接続情報
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# SSL証明書のパス
# ssl_cert = str(base_path / 'DigiCertGlobalRootCA.crt.pem')

# MySQLのURL構築
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# エンジンの作成（SSL設定を追加）
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)

    # connect_args={
    #     "ssl": {
    #         "ssl_ca": ssl_cert
    #     }
    # },

print("[DEBUG] DB_NAME =", DB_NAME)
print("[DEBUG] DATABASE_URL =", DATABASE_URL)
print("Current working directory:", os.getcwd())

# from sqlalchemy import create_engine
# import os
# from pathlib import Path
# from dotenv import load_dotenv

# # 環境変数の読み込み
# base_path = Path(__file__).parents[1]  # backendディレクトリへのパス
# # env_path = base_path / '.env'
# # load_dotenv(dotenv_path=env_path)

# # データベース接続情報
# DB_USER = os.getenv('DB_USER')
# DB_PASSWORD = os.getenv('DB_PASSWORD')
# DB_HOST = os.getenv('DB_HOST')
# DB_PORT = os.getenv('DB_PORT')
# DB_NAME = os.getenv('DB_NAME')

# # SSL証明書のパス
# ssl_cert = str(base_path / 'DigiCertGlobalRootCA.crt.pem')

# # MySQLのURL構築
# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# # エンジンの作成（SSL設定を追加）
# engine = create_engine(
#     DATABASE_URL,
#     connect_args={
#         "ssl": {
#             "ssl_ca": ssl_cert
#         }
#     },
#     echo=True,
#     pool_pre_ping=True,
#     pool_recycle=3600
# )

# from sqlalchemy import create_engine

# import os
# from dotenv import load_dotenv

# # 環境変数の読み込み
# load_dotenv()

# # データベース接続情報
# DB_USER = os.getenv('DB_USER')
# DB_PASSWORD = os.getenv('DB_PASSWORD')
# DB_HOST = os.getenv('DB_HOST')
# DB_PORT = os.getenv('DB_PORT')
# DB_NAME = os.getenv('DB_NAME')

# # MySQLのURL構築
# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# # エンジンの作成
# engine = create_engine(
#     DATABASE_URL,
#     echo=True,
#     pool_pre_ping=True,
#     pool_recycle=3600
# )
