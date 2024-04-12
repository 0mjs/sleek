# Sleekify
Sleekify is a minimalistic, highly-performant, asychronous Python REST API framework. It's been designed with simplicity as the main focus, aiming to provide a straightforward and efficient way to create robust Web API's, drawing inspiration from both Express.js and FastAPI.

## Features
- Simple & Expressive: Sleekify is easy to write, with simple expressive syntax.
- Async-first: Built on the asynchronous server methodology, enabling high performance and speed in concurrency.
- Flexible: Supports a wide range of request handling features from simple routes to complex parameter parsing.
- Validated: Uses `typing` to ensure your requests are properly validated and sanitised.
- Easy Setup: You can get up and running in just a few lines of code!

## Installation
Install using:

`pip`
```zsh
pip install sleekify
```

`conda`
```zsh
conda create --name my_env python=3.11 -y
conda activate sleekify
pip install sleekify
```

## Quick Start
To get started with Sleekify, you can set up a basic web application with several routes as shown below:

```python
from sleekify import App, Request
from pydantic import BaseModel

app = App()

class Item(BaseModel):
    name: str
    description: str
    price: float

@app.get("/")
async def home():
    return {"message": "Welcome to Sleekify!"}

@app.post("/")
async def create_item(request: Request):
    data = await request.json()
    return {"data": data}

@app.get("/item")
async def get_item(id: int):
    return {"message": f"Item: {id}"}

@app.put("/item/{id}")
async def update_item(request: Request, id: int):
    data = await request.json()
    return {"id": id, "updated_data": data}

@app.delete("/item/{id}")
async def delete_item(id: int):
    return {"message": f"Item {id} deleted successfully"}

@app.post("/items")
async def create_item(item: Item):
    return {"item": item.model_dump(), "message": "Item created successfully"}
```

## Running Your App
To run your Sleekify application, use an ASGI server such as Uvicorn:

```
pip install uvicorn
```

Then, replace `module_name` with the name of the Python file where your app is defined.
For example: If your `app` is in the root directory of your project, use: `uvicorn app:app --reload --port 8080`

```zsh
uvicorn module_name:app --reload --port 8080
```

## Running Tests
To run the Sleekify internal testing suite that uses `pytest-asyncio` and `httpx`, run the following command:

```zsh
pytest test/__init__.py
```

## Developer Start
- `pip install -r requirements.txt`
- `uvicorn app:app --reload --port 8080`
- `curl http://localhost:8080/hello`
- `pytest test/__init__.py`

## Documentation and Support
Documentation is currently being developed to better outline usage.
If you need support, please contact the developer directly: `dev@mattjs.me` / `https://x.com/0mjs_`