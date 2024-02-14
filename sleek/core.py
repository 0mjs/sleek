from typing import Dict, Callable, Awaitable

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import Scope, Receive, Send


class Sleek:
    def __init__(self):
        self.routes: Dict[
            str, Dict[str, Callable[[Request], Awaitable[JSONResponse]]]
        ] = {}

    def add_route(
        self,
        path: str,
        method: str,
        handler: Callable[[Request], Awaitable[JSONResponse]],
    ):
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method.upper()] = handler

    def get(self, path: str):
        def decorator(func: Callable[[Request], Awaitable[JSONResponse]]):
            self.add_route(path, "GET", func)
            return func

        return decorator

    def post(self, path: str):
        def decorator(func: Callable[[Request], Awaitable[JSONResponse]]):
            self.add_route(path, "POST", func)
            return func

        return decorator

    def put(self, path: str):
        def decorator(func: Callable[[Request], Awaitable[JSONResponse]]):
            self.add_route(path, "PUT", func)
            return func

        return decorator

    def delete(self, path: str):
        def decorator(func: Callable[[Request], Awaitable[JSONResponse]]):
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
                response = JSONResponse({"message": "Not Found"}, status_code=404)
            await response(scope, receive, send)
        else:
            raise NotImplementedError(f"Unsupported scope type {scope['type']}")
