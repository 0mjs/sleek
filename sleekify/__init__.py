from json.decoder import JSONDecodeError
from inspect import signature, _empty, isclass
from typing import Any, Dict, Callable, Awaitable, Optional, Union, get_type_hints
import asyncio

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import Scope, Receive, Send
from pydantic import BaseModel, ValidationError

RouteHandler = Callable[[Request], Awaitable[JSONResponse]]
RouterHandlerFunc = Callable[..., Awaitable[Union[JSONResponse, Dict]]]
Routes = Dict[str, Dict[str, RouteHandler]]


class Guard:
    def __init__(self, func: Callable[..., Awaitable[Any]], *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    async def resolve(self):
        if asyncio.iscoroutinefunction(self.func):
            return await self.func(*self.args, **self.kwargs)
        else:
            return self.func(*self.args, **self.kwargs)


class Sleekify:
    def __init__(self):
        self.routes: Routes = {}

    def router(
        self,
        path: str,
        method: str,
        handler: RouteHandler,
    ):
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method.upper()] = handler

    def get(self, path: str):
        def decorator(func: RouterHandlerFunc):
            async def handler(request: Request):
                sig = signature(func)
                if "request" in sig.parameters:
                    result = await func(request)
                else:
                    result = await func()

                if isinstance(result, Dict):
                    return JSONResponse(result)
                return result

            self.router(path, "GET", handler)
            return func

        return decorator

    def post(self, path: str):
        def decorator(func: RouterHandlerFunc):
            async def handler(request: Request):
                try:
                    json_body = await request.json()
                except JSONDecodeError:
                    json_body = {}

                sig = signature(func)
                kwargs = {}

                for name, param in sig.parameters.items():
                    if isinstance(param.default, Guard):
                        resolved_value = await param.default.resolve()
                        kwargs[name] = resolved_value
                    elif isclass(param.annotation) and issubclass(
                        param.annotation, BaseModel
                    ):
                        try:
                            model = param.annotation(**json_body)
                            kwargs[name] = model
                        except ValidationError as e:
                            return JSONResponse({"detail": e.errors()}, status_code=422)
                    else:
                        value = json_body.get(
                            name, param.default if param.default is not _empty else None
                        )
                        kwargs[name] = value

                response = await func(**kwargs)

                if isinstance(response, Dict):
                    return JSONResponse(response)
                return response

            self.router(path, "POST", handler)
            return func

        return decorator

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            path = scope["path"]
            method = scope["method"]
            handler = self.routes.get(path, {}).get(method.upper())

            try:
                if handler:
                    response = await handler(request)
                    if isinstance(response, Dict):
                        response = JSONResponse(response)
                    if isinstance(response, JSONResponse):
                        await response(scope, receive, send)
                    else:
                        raise TypeError(
                            "Response should be a dictionary or JSONResponse, dictionaries are inferred to JSONResponse."
                        )
                else:
                    response = JSONResponse({"message": "Not Found"}, status_code=404)
                    await response(scope, receive, send)
            except JSONDecodeError:
                response = JSONResponse(
                    {"detail": "Invalid JSONResponse."}, status_code=400
                )
                await response(scope, receive, send)
            except Exception as e:
                response = JSONResponse({"detail": str(e)}, status_code=400)
                await response(scope, receive, send)
