from functools import wraps

from sleekify.router import Router
from sleekify.requests import Request, Requests
from sleekify.responses import JSONResponse
from sleekify.util import match_path
from sleekify.const import METHODS


class App:
    def __init__(self):
        self.requests = Requests()
        self.router = Router()
        self.routes = {}

    def route(method: str):
        def decorator(func):
            @wraps(func)
            def wrapper(self, path: str):
                return self.router.route(self.routes, path, METHODS[method])

            return wrapper

        return decorator

    @route("get")
    def get(self):
        pass

    @route("post")
    def post(self):
        pass

    @route("put")
    def put(self):
        pass

    @route("patch")
    def patch(self):
        pass

    @route("delete")
    def delete(self):
        pass

    @route("options")
    def options(self):
        pass

    @route("head")
    def head(self):
        pass

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            path = scope["path"]
            method = scope["method"].upper()
            response = JSONResponse({"message": "Not Found"}, status_code=404)

            for route_path, methods in self.routes.items():
                match = match_path(route_path).match(path)
                if match:
                    path_params = match.groupdict()
                    return await self.requests.handler(
                        methods, method, request, path_params, scope, receive, send
                    )

            await response(scope, receive, send)
