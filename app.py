from sleek import API, Request, JSON

app = API()


@app.get("/")
async def get_endpoint():
    return JSON({"message": "Hello, world!"})


@app.post("/create")
async def post_endpoint(request: Request):
    body = await request.json()
    return JSON({"message": "Item created", "body": body})


from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    duration: int = 3600


@app.post("/pydantic")
async def pydantic_endpoint(item: ItemCreate):
    return JSON(
        {"message": "Data received", "name": item.name, "duration": item.duration}
    )
