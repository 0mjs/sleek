from typing import Any, Dict
import re
from json.decoder import JSONDecodeError
from inspect import signature, _empty, isclass

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import Scope, Receive, Send

from sleekify.guard import Guard
from sleekify.types import Router, Routes, RouteHandler
from pydantic import BaseModel, ValidationError


class App:
    def __init__(self):
        self.routes = {}

    def get(self, path: str):
        return self.route(path, "GET")

    def post(self, path: str):
        return self.route(path, "POST")

    def put(self, path: str):
        return self.route(path, "PUT")

    def patch(self, path: str):
        return self.route(path, "PATCH")

    def delete(self, path: str):
        return self.route(path, "DELETE")

    def router(self, path: str, method: str, handler: RouteHandler):
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method.upper()] = handler

    def route(self, path: str, method: str):
        def decorator(router: Router):
            async def handler(request: Request, **path_params):
                return await self.common(request, router, path_params)

            self.router(path, method, handler)
            return router

        return decorator

    async def resolver(self, request: Request, router: Router) -> Dict[str, Any]:
        sig = signature(router)
        kwargs = {}

        for name, param in sig.parameters.items():
            if param.annotation is Request:
                kwargs[name] = request
                continue

            if request.method in ["POST", "PUT", "PATCH"]:
                try:
                    json_body = await request.json()
                except JSONDecodeError:
                    json_body = {}

                if isinstance(param.default, Guard):
                    resolved_value = await param.default.resolve()
                    kwargs[name] = resolved_value
                elif isclass(param.annotation) and issubclass(
                    param.annotation, BaseModel
                ):
                    try:
                        model = param.annotation.parse_obj(json_body)
                        kwargs[name] = model
                    except ValidationError as e:
                        return JSONResponse({"detail": e.errors()}, status_code=422)
                else:
                    value = json_body.get(
                        name, param.default if param.default is not _empty else None
                    )
                    kwargs[name] = value
            else:
                for name, param in sig.parameters.items():
                    if name == "_request":
                        continue

        return kwargs

    async def common(self, request: Request, router: Router, path_params: dict = None):
        if path_params is None:
            path_params = {}

        kwargs = await self.resolver(request, router)
        kwargs.update(path_params)
        response = await router(**kwargs)

        if isinstance(response, Dict):
            return JSONResponse(response)
        elif isinstance(response, list):
            return JSONResponse(response)
        elif callable(response):
            return response
        else:
            return JSONResponse({"error": "Invalid response type"}, status_code=500)

    async def execute(
        self,
        handlers,
        method: str,
        request: Request,
        path_params: dict,
        scope: Scope,
        receive: Receive,
        send: Send,
    ):
        if handlers:
            handler = handlers.get(method)
            if handler:
                if path_params:
                    response = await handler(request, **path_params)
                else:
                    response = await handler(request)
                if isinstance(response, Dict):
                    response = JSONResponse(response)
                await response(scope, receive, send)
            else:
                allowed = ", ".join(handlers.keys())
                response = JSONResponse(
                    {"detail": "Method Not Allowed"},
                    status_code=405,
                    headers={"Allow": allowed},
                )
                await response(scope, receive, send)
        else:
            response = JSONResponse({"message": "Not Found"}, status_code=404)
            await response(scope, receive, send)

    def path_regex(self, path: str) -> str:
        pattern = re.sub(r"{(\w+)}", r"(?P<\1>[^/]+)", path)
        compiled_pattern = re.compile(f"^{pattern}$")
        return compiled_pattern

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            path = scope["path"]
            method = scope["method"].upper()
            matched = False

            for route_path, methods in self.routes.items():
                match = self.path_regex(route_path).match(path)
                if match:
                    path_params = match.groupdict()
                    handler = methods.get(method)
                    if handler:
                        response = await handler(request, **path_params)
                        await response(scope, receive, send)
                        matched = True
                        break
                    else:
                        response = JSONResponse(
                            {"detail": "Method Not Allowed"}, status_code=405
                        )
                        await response(scope, receive, send)
                        matched = True
                        break

            if not matched:
                response = JSONResponse({"message": "Not Found"}, status_code=404)
                await response(scope, receive, send)
