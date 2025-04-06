from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 新しいルーター（/answers）をインポート
from routers import answer

app = FastAPI()

# CORSミドルウェアの設定（ローカル開発用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて制限可能
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# トップページ（動作確認用）
@app.get("/")
def index():
    return {"message": "FastAPI Zukiraku API running!"}

# /answersルーターを登録（タイプ判定用API）
app.include_router(answer.router, prefix="", tags=["Headache Screening"])
