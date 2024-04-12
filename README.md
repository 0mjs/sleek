# Sleekify
Sleekify is a minimalistic, high-performance Python API framework built on top of Starlette. It is designed to provide a straightforward and efficient way to create web APIs, drawing inspiration from both Express.js and FastAPI.

## Features
- Simple and Expressive: Easy to write and understand syntax, allowing for quick setup and deployment of API services.
- ASGI-based: Built on the asynchronous server gateway interface provided by Starlette, enabling high concurrency and speed.
- Flexible: Supports a wide range of request handling features from simple routes to complex parameter parsing.

## Installation
Install Sleekify using pip:

```zsh
pip install sleekify
```

Alternatively, if you use Anaconda, you can set up a new environment for Sleekify:

```zsh
conda create --name sleekify python=3.8 -y
conda activate sleekify
pip install sleekify
```

## Requirements
Sleekify requires Python 3.6+ and relies on Starlette for the underlying ASGI support. Ensure all dependencies are installed by checking the requirements.txt file typically found in Python projects:

```zsh
pip install -r requirements.txt
```

## Quick Start
To get started with Sleekify, you can set up a basic web application with several routes as shown below:

```python
from sleekify import App, Request

app = App()

@app.get("/")
async def home():
    return {"message": "Welcome to Sleekify!"}

@app.post("/")
async def create_item(request: Request):
    data = await request.json()
    return {"data": data}

@app.put("/item/{id}")
async def update_item(request: Request, id: int):
    data = await request.json()
    return {"id": id, "updated_data": data}

@app.delete("/item/{id}")
async def delete_item(id: int):
    return {"message": f"Item {id} deleted successfully"}
```

## Running Your App
To run your Sleekify application, use an ASGI server such as Uvicorn:
(Replace module_name with the name of the Python file where your app is defined)

```zsh
uvicorn module_name:app --reload
```

## Advanced Usage
Sleekify supports complex routing, middleware integration, and request validation using Pydantic models:

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str
    price: float

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item.dict(), "message": "Item created successfully"}
```

## Documentation and Support
Documentation is currently being developed to better outline usage.
If you need support, please contact the developer directly: dev@mattjs.me