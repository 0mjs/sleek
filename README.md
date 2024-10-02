# Sleekify
Sleekify is a minimalistic and async-first Starlette-based REST API framework for Python. 

The framework focuses heavily on simplicity and developer experience (DX), aiming to provide a straightforward and efficient way to create robust Web API's, it draws inspiration from both Express.js and FastAPI.

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

app = App()

@app.get("/")
async def endpoint():
    return {"message": "Welcome to Sleekify!"}
```

## Running Your App
To run your Sleekify application, use an ASGI server such as Uvicorn:

```
pip install uvicorn
```

Then, replace `module_name` with the name of the Python file where your app is defined.
For example: If your `app` is in the root directory of your project, use: `uvicorn app:app --reload --port 8080`

```zsh
uvicorn module_name:app --reload
```

## Running Tests
To run the Sleekify internal testing suite that uses `pytest-asyncio` and `httpx`, run the following command:

```zsh
pytest test.py
```

## Developer Start
- `pip install -r requirements.txt`
- `uvicorn app:app --reload`
- `curl http://localhost:8000/hello`
- `pytest test.py`

## Documentation and Support
Documentation is currently being developed to better outline usage.
If you need support, please contact the developer directly: `dev@mattjs.me` / `https://x.com/0mjs_`
