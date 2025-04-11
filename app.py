from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

# ルーターのインポート
from routers import answer
from routers import reflection

# -------------------------------
# ロギング設定
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# アプリケーション作成
app = FastAPI()

# -------------------------------
# CORSミドルウェアの設定（ローカル開発用）
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて制限可能
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# エラーハンドリングミドルウェア
# -------------------------------
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception("未処理の例外が発生しました")
        raise e

# -------------------------------
# トップページ（動作確認用）
# -------------------------------
@app.get("/")
def index():
    logger.info("トップページにアクセスがありました")
    return {"message": "FastAPI Zukiraku API running!"}

# -------------------------------
# 各ルーターの登録
# -------------------------------
app.include_router(answer.router, prefix="", tags=["Headache Screening"])
app.include_router(reflection.router, prefix="", tags=["Reflection"])

