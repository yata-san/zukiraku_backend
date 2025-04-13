from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi.responses import JSONResponse
import traceback

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

# バリデーションエラーのログ出力
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import request_validation_exception_handler

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("⚠️ バリデーションエラー:", exc.errors())
    return await request_validation_exception_handler(request, exc)

# -------------------------------
# 🌐 CORSミドルウェアの設定（ローカル & 本番対応）
# - allow_origins=["*"] と allow_credentials=True の併用はNG（CORS仕様でブロックされる）
# - localhost:3000 は Next.js の dev サーバー用
# - 本番URL（例: VercelやAzure）も追加することで将来的に切り替え可能
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[  # 👇 安全な範囲で明示指定する（＊は使わない）
        "http://localhost:3000",  # ✅ 開発時のNext.jsローカルフロント
        # "https://zukiraku.vercel.app",  # ✅ （本番Vercel用：将来使うなら追加）
        "https://app-002-step3-2-node-oshima1.azurewebsites.net",  # ✅ Azure上のAPI本番URL
        
    ],
    allow_credentials=True,  # ✅ 認証付きの通信も許可（クッキーやトークン付きfetch）
    allow_methods=["*"],     # ✅ GET/POST/PUTなどすべて許可
    allow_headers=["*"],     # ✅ ヘッダーの制限なし（Content-Typeなどを許可）
)

# -------------------------------
# エラーハンドリングミドルウェア
# -------------------------------
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # エラーの詳細をログに書く（ファイル・行番号含む）
        error_trace = traceback.format_exc()
        logger.exception("未処理の例外が発生しました:\n%s", error_trace)

        # Swagger上で詳細表示
        return JSONResponse(
            status_code=500,
            content={"detail": error_trace}  # ← エラーの詳細なスタックトレース付き
        )

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
app.include_router(answer.router, prefix="/api", tags=["Headache Screening"])
app.include_router(reflection.router, prefix="/api", tags=["Reflection"])

