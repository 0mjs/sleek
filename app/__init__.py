from typing import Optional
from pydantic import BaseModel

from sleekify import App, Request

app = App()


class ItemModel(BaseModel):
    name: str
    price: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/items/{item_id}/batch/{batch}")
async def endpoint(item_id: str, batch: str):
    return {"item_id": item_id, "batch_id": batch}


## request argument only, showing how this defaults to query parameters
## /hello-name?name=Matt
@app.get("/hello-name")
async def endpoint(name: str):
    return {"message": f"Hello, {name}!"}


# Method specific routes


## GET
@app.get("/get-route")
async def get_route():
    return {"method": "GET"}


## POST
@app.post("/post-route")
async def post_route(request: Request):
    data = await request.json()
    return {"method": "POST", "data": data}


## PUT
@app.put("/put-route")
async def put_route(request: Request):
    data = await request.json()
    return {"method": "PUT", "data": data}


## PATCH
@app.patch("/patch-route")
async def patch_route(request: Request):
    data = await request.json()
    return {"method": "PATCH", "data": data}


## DELETE
@app.delete("/delete-route")
async def delete_route():
    return {"method": "DELETE"}


@app.post("/create-item")
async def create_item(request: Request):
    item = await request.json()
    item_model = ItemModel(**item)
    return {"message": "Item created.", "item": item_model.model_dump()}


@app.get("/query-route")
async def query_route(request: Request):
    query_params = dict(request.query_params)
    return {"method": "GET", "params": query_params}


@app.post("/form-route")
async def form_route(request: Request):
    form_data = await request.form()
    return {"method": "POST", "data": dict(form_data)}


@app.post("/upload-file")
async def upload_file(request: Request):
    form_data = await request.form()
    file_contents = await form_data["file"].read()
    return {"method": "POST", "file_size": len(file_contents)}


# @app.get("/protected-route")
# async def protected_route(request: Request):
#     auth = await Guard(Authenticate, with_token=True)(request)
#     return {"message": "You are authenticated", "user": auth["user"]}


# Guard/Authentication methods


# async def Authenticate(with_token: bool = False):
#     if with_token:
#         return {"user": "Matt", "token": "123456"}
#     return {"user": "Matt"}
