from typing import Awaitable, Callable, Dict, Union

from starlette.requests import Request
from starlette.responses import JSONResponse


TRouteHandler = Callable[[Request], Awaitable[JSONResponse]]

TRouter = Callable[..., Awaitable[Union[JSONResponse, Dict]]]

TRoutes = Dict[str, Dict[str, TRouteHandler]]
