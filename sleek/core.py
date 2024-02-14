from typing import Dict, Callable, Awaitable

from .http import Request, JSON
from pydantic import BaseModel, ValidationError
from starlette.types import Scope, Receive, Send
from inspect import signature


class Sleek:
    def __init__(self):
        self.routes: Dict[str, Dict[str, Callable[[Request], Awaitable[JSON]]]] = {}

    def add_route(
        self,
        path: str,
        method: str,
        handler: Callable[[Request], Awaitable[JSON]],
    ):
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method.upper()] = handler

    def get(self, path: str):
        def decorator(func: Callable[[Request], Awaitable[JSON]]):
            self.add_route(path, "GET", func)
            return func

        return decorator

    def post(self, path: str):
        def decorator(func: Callable[..., Awaitable[JSON]]):
            async def wrapper(request: Request):
                sig = signature(func)
                model_cls = None
                for _, param in sig.parameters.items():
                    if issubclass(param.annotation, BaseModel):
                        model_cls = param.annotation
                        break

                if model_cls:
                    try:
                        json_body = await request.json()
                        model_instance = model_cls(**json_body)
                        response = await func(model_instance)
                    except ValidationError as e:
                        return JSON({"detail": e.errors()}, status_code=422)
                else:
                    response = await func(request)
                return response

            self.add_route(path, "POST", wrapper)
            return func

        return decorator

    def put(self, path: str):
        def decorator(func: Callable[[Request], Awaitable[JSON]]):
            self.add_route(path, "PUT", func)
            return func

        return decorator

    def delete(self, path: str):
        def decorator(func: Callable[[Request], Awaitable[JSON]]):
            self.add_route(path, "DELETE", func)
            return func

        return decorator

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            path = scope["path"]
            method = scope["method"]
            handler = self.routes.get(path, {}).get(method.upper())
            if handler:
                response = await handler(request)
            else:
                response = JSON({"message": "Not Found"}, status_code=404)
            await response(scope, receive, send)
        else:
            raise NotImplementedError(f"Unsupported scope type {scope['type']}")
