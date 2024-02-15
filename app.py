from typing import Optional

from sleekify import Sleekify, Guard
from pydantic import BaseModel

app = Sleekify()


class HelloModel(BaseModel):
    name: str
    age: Optional[int]
    dob: Optional[str]


# GET


class AuthModel(BaseModel):
    user: str
    token: str | None


async def Authenticate(with_token: bool = True) -> AuthModel:
    if with_token:
        return AuthModel(user="Matt", token="sleekify-token-250396")
    return AuthModel(user="Matt", token=None)


@app.post("/secure")
async def secure_endpoint(auth=Guard(Authenticate, with_token=True)):
    user, token = auth.user, auth.token
    return {
        "message": f"Hello, {user}! Your token is '{token}'",
    }


@app.get("/hello")
async def hello():
    return {
        "message": "Hello, world!",
        "framework": "sleekify",
        "version": "0.0.2",
    }


# POST


@app.post("/hello-pydantic-model")
async def hello(data: HelloModel):
    return {
        "message": f"Hello, {data.name}! You are {data.age} years old and were born on {data.dob}",
        "framework": "sleekify",
        "version": "0.0.2",
    }


@app.post("/hello-basic-args")
async def hello(name: str, age: Optional[int] = None, dob: Optional[str] = None):
    return {
        "message": f"Hello, {name}! You are {age} years old and were born on {dob}",
        "framework": "sleekify",
        "version": "0.0.2",
    }
