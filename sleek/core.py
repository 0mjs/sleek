from typing import Dict, Callable, Awaitable, Union

from .http import Request, JSON

from pydantic import BaseModel, ValidationError
from starlette.types import Scope, Receive, Send
from inspect import signature
import inspect


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
        def decorator(func: Callable[..., Awaitable[Union[JSON, Dict]]]):
            async def wrapper(request: Request):
                sig = inspect.signature(func)
                if "request" in sig.parameters:
                    result = await func(request)
                else:
                    result = await func()

                if isinstance(result, Dict):
                    return JSON(result)
                return result

            self.add_route(path, "GET", wrapper)
            return func

        return decorator

    def post(self, path: str):
        def decorator(func: Callable[..., Awaitable[Union[JSON, Dict]]]):
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
                elif "request" in sig.parameters:
                    response = await func(request)
                else:
                    response = await func()

                if isinstance(response, Dict):
                    return JSON(response)
                return response

            self.add_route(path, "POST", wrapper)
            return func

        return decorator

    def put(self, path: str):
        return self._method_decorator(path, "PUT")

    def delete(self, path: str):
        return self._method_decorator(path, "DELETE")

    def _method_decorator(self, path: str, method: str):
        def decorator(func: Callable[..., Awaitable[Union[JSON, Dict]]]):
            async def wrapper(request: Request):
                sig = signature(func)
                if "request" in sig.parameters:
                    result = await func(request)
                else:
                    result = await func()

                if isinstance(result, Dict):
                    return JSON(result)
                return result

            self.add_route(path, method, wrapper)
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
                if isinstance(response, Dict):
                    response = JSON(response)
                if isinstance(response, JSON):
                    await response(scope, receive, send)
                else:
                    raise TypeError("Handler response must be a JSON or Dict")
            else:
                response = JSON({"message": "Not Found"}, status_code=404)
                await response(scope, receive, send)
        else:
            raise NotImplementedError(f"Unsupported scope type {scope['type']}")
