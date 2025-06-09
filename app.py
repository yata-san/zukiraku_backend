from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
from db_control import crud, mymodels
from typing import List
from sqlalchemy import text
from db_control.connect_MySQL import engine


app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "FastAPI top page!"}


@app.get("/items")
def read_one_item(code: str = Query(...)):
    # prd_masterテーブルを参照
    result = crud.myselect(mymodels.PrdMaster, code, key_name="CODE")
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None


class CartItem(BaseModel):
    CODE: str
    NAME: str
    PRICE: int
    PRD_ID: int
    qty: int

class PurchaseRequest(BaseModel):
    items: List[CartItem]
    subtotal: int
    total: int

@app.post("/purchase")
def purchase(req: PurchaseRequest):
    with engine.begin() as conn:
        # 1. trd_headerにINSERT
        result = conn.execute(
            text(
                "INSERT INTO trd_header (TOTAL_AMT, TOTAL_AMT_EX_TAX) VALUES (:total_amt, :total_amt_ex_tax)"
            ),
            {"total_amt": req.total, "total_amt_ex_tax": req.subtotal}
        )
        trd_id = result.lastrowid

        # 2. trd_detailに商品ごとにINSERT
        for idx, item in enumerate(req.items, start=1):
            conn.execute(
                text(
                    """
                    INSERT INTO trd_detail
                    (TRD_ID, DTL_ID, PRD_ID, PRD_CODE, PRD_NAME, PRD_PRICE, QUANTITY)
                    VALUES
                    (:trd_id, :dtl_id, :prd_id, :prd_code, :prd_name, :prd_price, :quantity)
                    """
                ),
                {
                    "trd_id": trd_id,
                    "dtl_id": idx,
                    "prd_id": item.PRD_ID,
                    "prd_code": item.CODE,
                    "prd_name": item.NAME,
                    "prd_price": item.PRICE,
                    "quantity": item.qty
                }
            )
    return {"status": "success", "trd_id": trd_id}
