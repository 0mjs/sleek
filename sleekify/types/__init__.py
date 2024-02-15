from typing import Awaitable, Callable, Dict, Union
from starlette.requests import Request
from starlette.responses import JSONResponse

RouteHandler = Callable[[Request], Awaitable[JSONResponse]]
Router = Callable[..., Awaitable[Union[JSONResponse, Dict]]]
Routes = Dict[str, Dict[str, RouteHandler]]
