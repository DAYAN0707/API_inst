# 既存の import に Response などを追加
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.responses import HTMLResponse, PlainTextResponse, FileResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# モデル定義（1つにまとめました）
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = 0.0

class ResponseItem(BaseModel):
    name: str
    price: float
    is_offer: bool = False

# --- 各エンドポイント（関数名はすべてバラバラにする必要があります） ---

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users/")
def read_users(limit: int = 10, active: bool = True):
    return {"limit": limit, "active": active}

@app.post("/items/", response_model=ResponseItem)
def create_item(item: Item):
    return ResponseItem(name=item.name, price=item.price, is_offer=item.tax > 0)

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID: must be positive.")
    return {"item_id": item_id}

@app.get("/search/")
def search_items(query: str = Query(..., min_length=3, max_length=50)):
    return {"query": query}

@app.get("/paginate/")
def paginate(page: int = Query(1, ge=1), size: int = Query(10, le=100)):
    return {"page": page, "size": size}

# ここが探している箇所です！
@app.get("/products/{product_id}")
def read_product(product_id: int):
    if product_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid product ID")
    return {"product_id": product_id}

# 4.1 ステータスコードの変更 (201 Createdを返す)
@app.post("/products/", status_code=201)
def create_product(item: Item):
    return item

# 4.2 HTMLレスポンス
@app.get("/html/", response_class=HTMLResponse)
def get_html():
    return "<h1>Hello, FastAPI HTML!</h1>"

# 4.2 プレーンテキストレスポンス
@app.get("/text/", response_class=PlainTextResponse)
def get_text():
    return "Hello, FastAPI plain text!"

# 5.1 カスタムヘッダーを持つレスポンス
@app.get("/custom-header/")
def custom_header(response: Response):
    response.headers["X-Custom-Header"] = "Custom value"
    return {"message": "Custom header added"}