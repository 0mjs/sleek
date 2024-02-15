from json.decoder import JSONDecodeError
from inspect import signature, _empty, isclass
from typing import Any, Dict

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import Scope, Receive, Send
from pydantic import BaseModel, ValidationError

from sleekify.guard import Guard
from sleekify.types import RouteHandler, Router, Routes


class Sleekify:
    def __init__(self):
        self.routes: Routes = {}

    def router(self, path: str, method: str, handler: RouteHandler):
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method.upper()] = handler

    async def resolve_parameters(
        self, request: Request, router: Router
    ) -> Dict[str, Any]:
        sig = signature(router)
        kwargs = {}

        if "_request" in sig.parameters:
            kwargs["_request"] = request

        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                json_body = await request.json()
            except JSONDecodeError:
                json_body = {}

            for name, param in sig.parameters.items():
                if name == "_request":
                    continue

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

    async def resolve_parameters(
        self, request: Request, router: Router
    ) -> Dict[str, Any]:
        sig = signature(router)
        kwargs = {}

        if "request" in sig.parameters:
            kwargs["request"] = request

        if request.method == "POST":
            try:
                json_body = await request.json()
            except JSONDecodeError:
                json_body = {}

            for name, param in sig.parameters.items():
                if name == "request":
                    continue

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
                if name == "request":
                    continue

        return kwargs

    async def common_handler(self, request: Request, router: Router):
        kwargs = await self.resolve_parameters(request, router)
        response = await router(**kwargs)

        if isinstance(response, Dict):
            return JSONResponse(response)
        return response

    def route_decorator(self, path: str, method: str):
        def decorator(router: Router):
            async def handler(request: Request):
                return await self.common_handler(request, router)

            self.router(path, method, handler)
            return router

        return decorator

    def get(self, path: str):
        return self.route_decorator(path, "GET")

    def post(self, path: str):
        return self.route_decorator(path, "POST")

    def put(self, path: str):
        return self.route_decorator(path, "PUT")

    def patch(self, path: str):
        return self.route_decorator(path, "PATCH")

    def delete(self, path: str):
        return self.route_decorator(path, "DELETE")

    async def call_handlers(
        self,
        handlers,
        method: str,
        request: Request,
        scope: Scope,
        receive: Receive,
        send: Send,
    ):
        if handlers:
            handler = handlers.get(method)
            if handler:
                response = await handler(request)
                if isinstance(response, Dict):
                    response = JSONResponse(response)
                await response(scope, receive, send)
            else:
                response = JSONResponse(
                    {"detail": "Method Not Allowed"}, status_code=405
                )
                await response(scope, receive, send)
        else:
            response = JSONResponse({"message": "Not Found"}, status_code=404)
            await response(scope, receive, send)

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            path = scope["path"]
            method = scope["method"].upper()
            handlers = self.routes.get(path)

            await self.call_handlers(handlers, method, request, scope, receive, send)
