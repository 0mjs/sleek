from sleek.core import Zephyr

from starlette.requests import Request
from starlette.responses import JSONResponse

app = Zephyr()


@app.get("/")
async def read_root():
    return JSONResponse({"message": "Hello, world!"})


@app.post("/create")
async def create_item(request: Request):
    body = await request.json()
    return JSONResponse({"message": "Item created", "body": body})
