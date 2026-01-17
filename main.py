from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# 3.1 データモデルの作成（POSTリクエスト用）
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = 0.0

@app.get("/")
def read_root():
    return {"Hello": "World"}

# 2.3 クエリパラメータの利用
@app.get("/users/")
def read_users(limit: int = 10, active: bool = True):
    return {"limit": limit, "active": active}

# 3.2 POSTリクエストの受け取り
@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}

from fastapi import HTTPException # これを1行目の from fastapi import ... に追加するか、ここに書いてください

# 4.1 カスタムエラーメッセージ
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id < 0:
        # IDがマイナスの時に 400エラーを投げる
        raise HTTPException(status_code=400, detail="Invalid ID: must be positive.")
    return {"item_id": item_id}

# 4.2 レスポンスモデルの指定
class ResponseItem(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items/", response_model=ResponseItem)
def create_item(item: Item):
    # 送られてきたtax（税金）が0より大きければオファーあり(True)とするロジック
    return ResponseItem(name=item.name, price=item.price, is_offer=item.tax > 0)

from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID: must be positive.")
    return {"item_id": item_id}

# 5.1 必須パラメータとオプションパラメータ（文字数制限付き）
@app.get("/search/")
def search_items(query: str = Query(..., min_length=3, max_length=50)):
    return {"query": query}

# 5.2 デフォルト値と範囲指定（数値の制限付き）
@app.get("/paginate/")
def paginate(page: int = Query(1, ge=1), size: int = Query(10, le=100)):
    return {"page": page, "size": size}