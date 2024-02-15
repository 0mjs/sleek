# Sleekify
A minimalistic, ASGI, Python framework for building REST API's.
Heavily inspired by Express.js and FastAPI.

In it's absolute infancy, Sleekify already includes some common concepts of a REST API framework, such as routing, parameter resolution, serialisation, request handling, and response generation.

```
pip install sleekify
```

```
from sleekify import Sleekify

app = Sleekify()

app.post("/")
async def endpoint(name: str):
  return { "name": name }
```
  
