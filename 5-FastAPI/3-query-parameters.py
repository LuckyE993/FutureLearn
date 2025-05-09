from fastapi import FastAPI
from typing import Union, Optional

app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 0):
    return fake_items_db[skip: skip + limit]


@app.get("/items/{item_id}")  # FastAPI 可以识别出 item_id 是路径参数，q 不是路径参数，而是查询参数。
async def read_item(item_id: int, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"item_name": "Long Name123123213123123"})
    else:
        item.update({"item_name": "Short Name"})
    return item


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: str, item_id: int, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id, "user_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"item_name": "Long Name123123213123123"})
    else:
        item.update({"item_name": "Short Name"})
    return item
