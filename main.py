from fastapi import FastAPI, HTTPException, Query, Response, Depends, status
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# ===== モデル =====
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = 0.0

class ResponseItem(BaseModel):
    name: str
    price: float
    is_offer: bool = False

# ===== 認証依存関数 =====
def get_current_user(token: str = Query(None)):
    if token != "valid-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無効なトークンです"
        )
    return {"user": "authenticated_user"}

# ===== 設定依存関数 =====
def get_settings():
    return {"setting_value": "some setting"}


# ===== エンドポイント =====

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users/")
def read_users(limit: int = 10, active: bool = True):
    return {"limit": limit, "active": active}

@app.post("/items/", response_model=ResponseItem)
def create_item(item: Item):
    return ResponseItem(name=item.name, price=item.price, is_offer=item.tax > 0)

@app.get("/search/")
def search_items(query: str = Query(..., min_length=3, max_length=50)):
    return {"query": query}

@app.get("/paginate/")
def paginate(page: int = Query(1, ge=1), size: int = Query(10, le=100)):
    return {"page": page, "size": size}

@app.get("/products/{product_id}")
def read_product(product_id: int):
    if product_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid product ID")
    return {"product_id": product_id}

@app.post("/products/", status_code=201)
def create_product(item: Item):
    return item

@app.get("/html/", response_class=HTMLResponse)
def get_html():
    return "<h1>Hello, FastAPI HTML!</h1>"

@app.get("/text/", response_class=PlainTextResponse)
def get_text():
    return "Hello, FastAPI plain text!"

@app.get("/custom-header/")
def custom_header(response: Response):
    response.headers["X-Custom-Header"] = "Custom value"
    return {"message": "Custom header added"}

# ===== 認証と設定を使うエンドポイント（依存関係注入） =====

@app.get("/items/details")
def read_item_details(
    settings: dict = Depends(get_settings),
    user: dict = Depends(get_current_user)
):
    return {"settings": settings, "user": user}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID: must be positive.")
    return {"item_id": item_id}

@app.get("/users/me")
def read_current_user(user: dict = Depends(get_current_user)):
    return user

from contextlib import contextmanager
from fastapi import Depends

# ===== データベース接続管理の依存関数 =====
from fastapi import Depends

def get_db():
    db = "Database connection"
    print("Open DB")
    try:
        yield db
    finally:
        print("Close DB")

@app.get("/db/")
def read_data(db=Depends(get_db)):
    return {"db_status": db}





