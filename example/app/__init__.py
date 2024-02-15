from sleekify import App, Guard, Request
from pydantic import BaseModel
from typing import Optional

app = App()


class ItemModel(BaseModel):
    name: str
    price: Optional[int] = None


async def Authenticate(with_token: bool = False):
    if with_token:
        return {"user": "Matt", "token": "123456"}
    return {"user": "Matt"}


@app.get("/test1")
async def matt(request: Request):
    print(request.headers)
    body = await request.json()
    return {"body": body}


@app.post("/secure")
async def secure(auth=Guard(Authenticate, with_token=True)):
    return {"role": "authenticated", "session": auth}


@app.get("/get-items")
async def get():
    return {"data": ["item-1", "item-2", "item-3"]}


@app.get("/get-item/{id}")
async def endpoint(id: str):
    if id == "1":
        return {"data": "item-1"}
    return {"error": "Item not found"}


@app.get("/matt")
async def matt(request: Request):
    body = await request.json()
    return {"body": body}


@app.post("/matt")
async def matt(request: Request):
    body = await request.json()
    return {"body": body}


@app.put("/matt")
async def matt(request: Request):
    body = await request.json()
    return {"body": body}


@app.patch("/matt")
async def matt(request: Request):
    body = await request.json()
    return {"body": body}


@app.delete("/matt")
async def matt(request: Request):
    body = await request.json()
    return {"body": body}


@app.post("/create-item")
async def create(item: ItemModel):
    return {"data": f"item-{item.name}"}
