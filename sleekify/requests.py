from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import Scope, Receive, Send

from typing import Dict


class Requests:
    async def handler(
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
