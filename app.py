from sleek import App, Request, JSON
from pydantic import BaseModel


app = App()


class ItemCreate(BaseModel):
    name: str
    duration: int = 3600


@app.get("/")
async def get_endpoint():
    return {"message": "Hello, world!"}


@app.post("/create")
async def post_endpoint(request: Request):
    return JSON({"message": "Item created", "body": request})


@app.post("/pydantic")
async def pydantic_endpoint(item: ItemCreate):
    return JSON(
        {"message": "Data received", "name": item.name, "duration": item.duration}
    )
