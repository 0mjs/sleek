# Sleekify
A minimalistic, highly-performant Python API framework built on Starlette. Heavily inspired by Express.js and FastAPI.

Installation:

```
pip install sleekify
```

Usage:

```

from sleekify import App

app = App()

app.post("/")
async def endpoint(name: str):
  return { "name": name }

```

Get started:

Anaconda:

```
conda create --name sleekify -y && conda activate sleekify && pip install -r requirements.txt
```
