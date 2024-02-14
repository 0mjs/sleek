from json.decoder import JSONDecodeError
from typing import Optional

from core import Sleekify
from starlette.exceptions import HTTPException
from pydantic import BaseModel

app = Sleekify()


class HelloModel(BaseModel):
    name: str
    age: Optional[int]
    dob: Optional[str]


@app.get("/hello")
async def hello():
    return {"message": "Hello, world!"}


@app.post("/hello-pydantic-model")
async def hello(data: HelloModel):
    try:
        return {
            "message": f"Hello, {data.name}! You are {data.age} years old and were born on {data.dob}"
        }
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")


@app.post("/hello-basic-args")
async def hello(name: str, age: Optional[int] = None, dob: Optional[str] = None):
    try:
        return {
            "message": f"Hello, {name}! You are {age} years old and were born on {dob}"
        }
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
