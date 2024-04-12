from typing import Optional
from pydantic import BaseModel
from sleekify import App, Guard, Request

app = App()


class ItemModel(BaseModel):
    name: str
    price: Optional[int] = None


# GET


## no arguments, showing how we return JSONResponse() implicitly
@app.get("/hello")
async def endpoint():
    return {"message": f"Hello world!"}


## request argument, showing that it's there by default on all endpoints
@app.get("/hello-scope")
async def endpoint(request: Request):
    return {"message": f"Hello world! - {request.scope}"}


# path parameter, showing how we can use it in the endpoint
@app.get("/hello/{id}")
async def endpoint(id: str):
    return {"message": f"Hello, {id}!"}


## request argument only, showing how this defaults to query parameters
@app.get("/hello-scope-id")
async def endpoint(request: Request, id: str):
    return {"message": f"Hello, {id}! - {request.scope}"}


## path parameter and request argument, showing both in use together
@app.get("/hello-scope/{id}")
async def endpoint(request: Request, id: str):
    return {"message": f"Hello, {id}! - {request.scope}"}


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
    return {"item": item_model.model_dump(), "message": "Item created successfully"}


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


@app.get("/protected-route")
async def protected_route(request: Request):
    auth = await Guard(Authenticate, with_token=True)(request)
    return {"message": "You are authenticated", "user": auth["user"]}


# Guard/Authentication methods


async def Authenticate(with_token: bool = False):
    if with_token:
        return {"user": "Matt", "token": "123456"}
    return {"user": "Matt"}
