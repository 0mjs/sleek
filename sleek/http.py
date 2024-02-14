from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse as StarletteJSONResponse


class Request(StarletteRequest):
    pass


class JSON(StarletteJSONResponse):
    pass
