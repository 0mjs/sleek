from typing import Optional
from pydantic import BaseModel
from sleekify import App, Guard, Request

app = App()


class ItemModel(BaseModel):
    name: str
    price: Optional[int] = None


async def Authenticate(with_token: bool = False):
    if with_token:
        return {"user": "Matt", "token": "123456"}
    return {"user": "Matt"}


@app.get("/get-route")
async def get_route():
    return {"method": "GET"}


@app.post("/post-route")
async def post_route(request: Request):
    data = await request.json()
    return {"method": "POST", "data": data}


@app.put("/put-route")
async def put_route(request: Request):
    data = await request.json()
    return {"method": "PUT", "data": data}


@app.patch("/patch-route")
async def patch_route(request: Request):
    data = await request.json()
    return {"method": "PATCH", "data": data}


@app.delete("/delete-route")
async def delete_route():
    return {"method": "DELETE"}


@app.post("/secure-post")
async def secure_post(auth=Guard(Authenticate, with_token=True)):
    return {"role": "authenticated", "session": auth}


@app.post("/create-item")
async def create_item(item: ItemModel):
    return {"item": item.dict(), "message": "Item created successfully"}
