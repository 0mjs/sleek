# Sleekify
A minimalistic, ASGI, Python framework for building REST API's.
Heavily inspired by Express.js and FastAPI.

```
pip install sleekify
```

```
from sleekify import Sleekify
from pydantic import BaseModel

app = Sleekify()

class ItemModel(BaseModel):
  name: str

app.post("/create-item")
async def create_item(item: ItemModel):
  return { "name": item.name }
```
  
