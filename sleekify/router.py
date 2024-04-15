from typing import Any, Dict
from json.decoder import JSONDecodeError
from inspect import signature, _empty, isclass

from starlette.requests import Request
from starlette.responses import JSONResponse

from sleekify.guards import Guard
from sleekify._types import TRouter, TRoutes, TRouteHandler
from pydantic import BaseModel, ValidationError


class Router:
    def route(self, routes: TRoutes, path: str, method: Dict):
        return self.route_decorator(routes, path, method)

    def register_route(
        self, routes: TRoutes, path: str, method: str, handler: TRouteHandler
    ):
        if path not in routes:
            routes[path] = {}
        routes[path][method.upper()] = handler
        print(f"{path} ({method.upper()})")

    def route_decorator(self, routes: TRoutes, path: str, method: str):
        def decorator(router: TRouter):
            async def handler(request: Request, **path_params):
                return await self.route_handler(request, router, path_params)

            self.register_route(routes, path, method, handler)
            return router

        return decorator

    async def resolver(self, request: Request, router: TRouter) -> Dict[str, Any]:
        sig = signature(router)
        kwargs = {}

        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                json_body = await request.json()
            except JSONDecodeError:
                json_body = {}

            for name, param in sig.parameters.items():
                if param.annotation is Request:
                    kwargs[name] = request
                    continue

                if isinstance(param.default, Guard):
                    resolved_value = await param.default.resolve()
                    kwargs[name] = resolved_value
                elif isclass(param.annotation) and issubclass(
                    param.annotation, BaseModel
                ):
                    try:
                        model = param.annotation.model_validate(json_body)
                        kwargs[name] = model
                    except ValidationError as e:
                        return JSONResponse({"detail": e.errors()}, status_code=422)
                else:
                    value = json_body.get(
                        name, param.default if param.default is not _empty else None
                    )
                    kwargs[name] = value

        else:
            query_params = request.query_params
            for name, param in sig.parameters.items():
                if param.annotation is Request:
                    kwargs[name] = request
                    continue

                value = query_params.get(
                    name, param.default if param.default is not _empty else None
                )
                kwargs[name] = value

        return kwargs

    async def route_handler(
        self, request: Request, router: TRouter, path_params: dict = None
    ):
        if path_params is None:
            path_params = {}

        kwargs = await self.resolver(request, router)
        kwargs.update(path_params)
        response = await router(**kwargs)

        if (
            isinstance(response, Dict)
            or isinstance(response, BaseModel)
            or isinstance(response, list)
        ):
            return JSONResponse(response)
        elif callable(response):
            return response
        else:
            return JSONResponse({"error": "Invalid response type"}, status_code=500)
