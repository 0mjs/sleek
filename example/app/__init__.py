from sleekify import Sleekify, Guard, Request
from pydantic import BaseModel
from typing import Optional

app = Sleekify()


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
async def secure(auth=Guard(Authenticate, with_token=False)):
    return {"role": "authenticated", "session": auth}


# @app.get("/get-item")
# async def get():
#     return {"data": "item-1"}


@app.get("/matt")
async def matt(request: Request):
    body = await request.json()
    return {"body": body}


# @app.post("/matt")
# async def matt(request: Request):
#     body = await request.json()
#     return {"body": body}


# @app.put("/matt")
# async def matt(request: Request):
#     body = await request.json()
#     return {"body": body}


# @app.patch("/matt")
# async def matt(request: Request):
#     body = await request.json()
#     return {"body": body}


# @app.delete("/matt")
# async def matt(request: Request):
#     body = await request.json()
#     return {"body": body}


# @app.post("/create-item")
# async def create(item: ItemModel):
#     return {"data": f"item-{item.name}"}
