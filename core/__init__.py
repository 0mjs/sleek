from json.decoder import JSONDecodeError
from inspect import signature, _empty, isclass
from typing import Dict, Callable, Awaitable, Optional, Union, get_type_hints

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import Scope, Receive, Send
from pydantic import BaseModel, ValidationError


class Sleekify:
    def __init__(self):
        self.routes: Dict[
            str, Dict[str, Callable[[Request], Awaitable[JSONResponse]]]
        ] = {}

    def router(
        self,
        path: str,
        method: str,
        handler: Callable[[Request], Awaitable[JSONResponse]],
    ):
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method.upper()] = handler

    def get(self, path: str):
        def decorator(func: Callable[..., Awaitable[Union[JSONResponse, Dict]]]):
            async def wrapper(request: Request):
                sig = signature(func)
                if "request" in sig.parameters:
                    result = await func(request)
                else:
                    result = await func()

                if isinstance(result, Dict):
                    return JSONResponse(result)
                return result

            self.router(path, "GET", wrapper)
            return func

        return decorator

    def post(self, path: str):
        def decorator(func: Callable[..., Awaitable[Union[JSONResponse, Dict]]]):
            async def wrapper(request: Request):
                try:
                    json_body = await request.json()
                except JSONDecodeError:
                    return JSONResponse({"detail": "Invalid JSON."}, status_code=400)

                sig = signature(func)
                type_hints = get_type_hints(func)
                kwargs = {}

                for name, param in sig.parameters.items():
                    param_type = type_hints.get(name)
                    if isclass(param_type) and issubclass(param_type, BaseModel):
                        try:
                            model = param_type(**json_body)
                            kwargs[name] = model
                        except ValidationError as e:
                            return JSONResponse({"detail": e.errors()}, status_code=422)
                    else:
                        if name in json_body:
                            kwargs[name] = json_body[name]
                        elif param.default is not _empty:
                            kwargs[name] = param.default
                        elif param.annotation in [Optional, Union]:
                            kwargs[name] = None

                response = await func(**kwargs)

                if isinstance(response, Dict):
                    return JSONResponse(response)
                return response

            self.router(path, "POST", wrapper)
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
                        raise TypeError("Handler response must be JSONResponse or Dict")
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
